"""
CMS

"""
import os
import datetime
import json
from flask import url_for, request, redirect, abort, session, jsonify
from webportfolio import WebPortfolio, route, storage, nav_menu, \
    flash_success, flash_data, get_flashed_data, flash_error, ModelError
from webportfolio import utils, wp_markdown
from flask_login import login_required, current_user
from paginator import Paginator

WebPortfolio.register_module(__name__)

def model(UserModel):
    """
    Post Model
    :param UserModel:
    """

    db = UserModel.User.db

    class SlugNameMixin(object):
        name = db.Column(db.String(255), index=True)
        slug = db.Column(db.String(255), index=True, unique=True)
        description = db.Column(db.String(255))
        image_url = db.Column(db.Text)

        @classmethod
        def get_by_slug(cls, slug=None, name=None):
            """
            Return a post by slug
            """
            if name and not slug:
                slug = utils.slugify(name)
            return cls.all().filter(cls.slug == slug).first()

        @classmethod
        def new(cls, name, slug=None):
            slug = utils.slugify(name if not slug else slug)
            return cls.create(name=name, slug=slug)

        def rename(self, name, slug=None):
            slug = utils.slugify(name if not slug else slug)
            return self.update(name=name, slug=slug)

    class CmsType(SlugNameMixin, db.Model):
        """
        Types
        """
        @property
        def total_posts(self):
            return CmsPost.all().filter(CmsPost.type_id == self.id).count()

    class CmsCategory(SlugNameMixin, db.Model):
        """
        Category
        """
        @property
        def total_posts(self):
            return CmsCategoryMap.all()\
                .filter(CmsCategoryMap.category_id == self.id)\
                .count()

    class CmsTag(SlugNameMixin, db.Model):
        """
        Tag
        """
        @property
        def total_posts(self):
            return CmsTagMap.all()\
                .filter(CmsTagMap.tag_id == self.id)\
                .count()

    class CmsTagMap(db.Model):
        """
        PostPostTag
        """
        post_id = db.Column(db.Integer, db.ForeignKey("cms_post.id"))
        tag_id = db.Column(db.Integer, db.ForeignKey(CmsTag.id))

        @classmethod
        def add(cls, post_id, tag_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.tag_id == tag_id)\
                .first()
            if not c:
                cls.create(post_id=post_id, tag_id=tag_id)

        @classmethod
        def remove(cls, post_id, tag_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.tag_id == tag_id)\
                .first()
            if c:
                c.delete(hard_delete=True)

    class CmsCategoryMap(db.Model):
        post_id = db.Column(db.Integer, db.ForeignKey("cms_post.id"))
        category_id = db.Column(db.Integer, db.ForeignKey(CmsCategory.id))

        @classmethod
        def add(cls, post_id, category_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.category_id == category_id)\
                .first()
            if not c:
                cls.create(post_id=post_id, category_id=category_id)

        @classmethod
        def remove(cls, post_id, category_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.category_id == category_id)\
                .first()
            if c:
                c.delete(hard_delete=True)

    class CmsPost(db.Model):

        user_id = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
        type_id = db.Column(db.Integer, db.ForeignKey(CmsType.id))

        title = db.Column(db.String(255))
        slug = db.Column(db.String(255), index=True)
        content = db.Column(db.Text)
        description = db.Column(db.Text)
        featured_image = db.Column(db.Text)
        featured_embed = db.Column(db.Text)
        featured_media_top = db.Column(db.String(10))
        language = db.Column(db.String(255))
        parent_id = db.Column(db.Integer)  # If the post is derived from another post
        is_child = db.Column(db.Boolean, index=True, default=False)  #
        is_list = db.Column(db.Boolean, index=True, default=False)  # A list is a type of post having sub post
        is_featured = db.Column(db.Boolean, index=True, default=False)  # Feature post are limited
        featured_at = db.Column(db.DateTime)
        is_sticky = db.Column(db.Boolean, index=True, default=False)  # A sticky post usually stay on top, no matter the count
        sticky_at = db.Column(db.DateTime)
        is_published = db.Column(db.Boolean, index=True, default=True)
        published_at = db.Column(db.DateTime)
        published_by = db.Column(db.Integer)
        is_revision = db.Column(db.Boolean, default=False)
        revision_id = db.Column(db.Integer)  # When updating the post, will auto-save

        is_public = db.Column(db.Boolean, index=True, default=False)
        is_draft = db.Column(db.Boolean, index=True, default=False)
        options_data = db.Column(db.Text, default="{}")
        menu_order = db.Column(db.Integer, default=0, index=True)

        author = db.relationship(UserModel.User, backref="posts")
        type = db.relationship(CmsType, backref="posts")
        categories = db.relationship(CmsCategory,
                                     secondary=CmsCategoryMap.__table__.name)
        tags = db.relationship(CmsTag,
                                     secondary=CmsTagMap.__table__.name)

        @classmethod
        def new(cls, title, **kwargs):
            """
            Insert a new post
            """
            published_date = None
            is_revision = False
            is_published = False
            is_draft = False
            is_public = kwargs.get("is_public", True)
            parent_id = kwargs.get("parent_id", None)

            if kwargs.get("is_revision"):
                if not parent_id:
                    raise ModelError("'parent_id' is missing for revision")
                is_revision = True
                is_public = False
            elif kwargs.get("is_draft"):
                is_draft = True
                is_public = False
            elif kwargs.get("is_published"):
                is_published = True
                published_date = datetime.datetime.now()

            slug = None
            if is_published or is_draft:
                slug = cls.create_slug(kwargs.get("slug", title))

            type_id = kwargs.get("type_id")
            if not type_id and kwargs.get("type_slug"):
                type_slug = kwargs.get("type_slug")
                _type = CmsType.get_by_slug(slug=type_slug)
                if _type:
                    type_id = _type.id

            data = {
                "user_id": kwargs.get("user_id", 0),
                "title": title,
                "slug": slug,
                "content": kwargs.get("content"),
                "description": kwargs.get("description"),
                "is_published": is_published,
                "published_at": published_date,
                "is_draft": is_draft,
                "is_revision": is_revision,
                "is_public": is_public,
                "parent_id": parent_id,
                "type_id": type_id
            }
            return cls.create(**data)

        @classmethod
        def get_published(cls, id=None, slug=None, types=[], categories=[], tags=[]):
            """
            Return published posts.
            If $id or $slug it will return a single post, else all

            :param id: int - the id of a post
            :param slug: string - the slug of a post
            :param types: list - list of types slugs
            :param categories: list - list of categories slug
            :param tags: list - list of tags slugs
            :return:
            """
            q = cls.all().filter(cls.is_published == True)

            # Query only a single post
            if id or slug:
                if id:
                    q = q.filter(cls.id == id)
                elif slug:
                    q = q.filter(cls.slug == slug)
                return q.first()

            # Query lists
            else:
                if types:
                    q = q.join(CmsType)\
                        .filter(CmsType.slug.in_(types))
                if categories:
                    q = q.join(CmsCategoryMap)\
                        .join(CmsCategory)\
                        .filter(CmsCategory.slug.in_(categories))
                if tags:
                    q = q.join(CmsTag)\
                        .filter(CmsTag.slug.in_(tags))
                return q

        @classmethod
        def create_slug(cls, title):
            slug = None
            slug_counter = 0
            _slug = utils.slugify(title).lower()
            while True:
                slug = _slug
                if slug_counter > 0:
                    slug += str(slug_counter)
                slug_counter += 1
                if not cls.get_by_slug(slug):
                    break
            return slug

        @classmethod
        def get_by_slug(cls, slug):
            """
            Return a post by slug
            """
            return cls.all().filter(cls.slug == slug).first()

        def publish(self, published_date=None, published_by_id=None):
            if self.is_draft:
                data = {
                    "is_draft": False,
                    "is_published": True,
                    "published_at": published_date or datetime.datetime.now()
                }
                if published_by_id:
                    data.update({
                        "published_by": published_by_id
                    })

                self.update(**data)

        def set_slug(self, title):
            slug = utils.slugify(title)
            if title and slug != self.slug:
                slug = self.create_slug(slug)
                self.update(slug=slug)

        def update_categories(self, categories_list):
            """
            Update categories by replacing existing list with new list
            :param categories_list: list. The new list of category
            """
            cats = CmsCategoryMap.all()\
                    .filter(CmsCategoryMap.post_id == self.id)
            cats_list = [c.category_id for c in cats]

            del_cats = list(set(cats_list) - set(categories_list))
            new_cats = list(set(categories_list) - set(cats_list))

            for dc in del_cats:
                CmsCategoryMap.remove(post_id=self.id, category_id=dc)

            for nc in new_cats:
                CmsCategoryMap.add(post_id=self.id, category_id=nc)

        def update_tags(self, tags_list):
            """
            Update tags by replacing existing list with new list
            :param tags_list: list. The new list of tags
            """
            tags = CmsTagMap.all()\
                    .filter(CmsTagMap.post_id == self.id)
            tags_list_ = [c.tag_id for c in tags]

            del_tags = list(set(tags_list_) - set(tags_list))
            new_tags = list(set(tags_list) - set(tags_list_))

            for dc in del_tags:
                CmsTagMap.remove(post_id=self.id, tag_id=dc)

            for nc in new_tags:
                CmsTagMap.add(post_id=self.id, tag_id=nc)

        def get_list(self):
            if not self.is_list:
                return None

            return CmsPost.all()\
                .filter(CmsPost.is_published == True)\
                .filter(CmsPost.is_child == True)\
                .filter(CmsPost.parent_id == self.id)

        def delete_revisions(self):
            """
            Delete all revisions
            """
            try:
                CmsPost.all()\
                    .filter(CmsPost.post_id == self.id)\
                    .filter(CmsPost.is_revision == True)\
                    .delete()
                CmsPost.db.commit()
            except Exception as ex:
                CmsPost.db.rollback()

        def set_options(self, key, values):
            options = self.options
            options.update({key: values})
            self.update(options_data=json.dumps(options))

        @property
        def options(self):
            return json.loads(self.options_data) if self.options_data else {}

        @property
        def excerpt(self):
            """
            Return description as excerpt, if empty,
            it will return the first paragraph
            :return: str
            """
            if self.description:
                return self.description
            else:
                return ""

        @property
        def top_image(self):
            """
            Return the top image
            Return the image url if exists, or it will get the first image
            Will get the first image from the markdown
            """
            if self.featured_image:
                return self.featured_image
            elif self.content:
                md_images = wp_markdown.extract_images(self.content)
                return md_images[0] if md_images else None

        @property
        def status(self):
            if self.is_published:
                return "Published"
            elif self.is_draft:
                return "Draft"
            elif self.is_revision:
                return "Revision"
            else:
                return ""

        @property
        def total_revisions(self):
            return CmsPost.all()\
                .filter(CmsPost.post_id == self.id)\
                .filter(CmsPost.is_revision == True)\
                .count()

    class CmsUploadObject(db.Model):
        parent_id = db.Column(db.Integer, index=True)
        user_id = db.Column(db.Integer, index=True)
        provider = db.Column(db.String(255))
        container = db.Column(db.String(255))
        local_path = db.Column(db.Text)
        name = db.Column(db.Text)
        description = db.Column(db.String(255))
        size = db.Column(db.Integer)
        extension = db.Column(db.String(10), index=True)
        type = db.Column(db.String(25), index=True)
        object_path = db.Column(db.Text)
        object_url = db.Column(db.Text)
        is_private = db.Column(db.Boolean, index=True, default=False)

    return utils.to_struct(Post=CmsPost,
                           Category=CmsCategory,
                           Type=CmsType,
                           CategoryMap=CmsCategoryMap,
                           Tag=CmsTag,
                           TagMap=CmsTagMap,
                           UploadObject=CmsUploadObject)

# ------------------------------------------------------------------------------

def post(view, **kwargs):
    """
    It extends your view  read, list content from the CMS

    kwargs:
        model: class
        templates_dir: str - The directory of templates
        query: dict
            - types: list of types to show
            - order_by: str - of order by
        endpoints: dict
            - {
                $action_name: {
                    - endpoint: The endpoint to use for the action
                    - menu: The name of the menu
                    - show_menu: bool - show/hide menu
                    - menu_order: int - position of the menu
                    - title:
                    - image
                }
            }, ...
    """

    # Setting up endpoint config, for url based
    # It will be used to access the proper endpoint and format the
    endpoints_config = {
        "id": {
            "url": "{id}",
            "accept": ["id"]
        },
        "slug": {
            "url": "{slug}",
            "accept": ["slug"]
        },
        "id-slug": {
            "url": "{id}/{slug}",
            "accept": ["id", "slug"]
        },
        "month-slug": {
            "url": "{month}/{slug}",
            "accept": ["month", "slug"]
        },
        "date-slug": {
            "url": "{date}/{slug}",
            "accept": ["date", "slug"]
        }
    }
    endpoints_config = utils.DotDict(endpoints_config)

    # Totally required
    model = kwargs.get("model")

    # templates directory
    templates_dir = kwargs.get("templates_dir", "WebPortfolio/Module/Cms/Post")

    # query
    opt_queries = utils.DotDict(kwargs.get("query", {}))
    post_types = opt_queries.get("types", [])
    post_categories = opt_queries.get("categories", [])
    post_tags = opt_queries.get("categories", [])
    post_order_by = opt_queries.get("order_by", "published_at desc")
    post_per_page = opt_queries.get("per_page", 20)

    # endpoints
    opt_endpoints = utils.DotDict(kwargs.get("endpoints", {}))

    # The single.endpoint accept an extra param to format the post read
    # :slug
    # endpoint:url
    single_endpoint_url = "slug"
    single_endpoint = opt_endpoints.get("single.endpoint", "post:slug")
    if ":" in single_endpoint:
        single_endpoint, single_endpoint_url = single_endpoint.split(":", 2)
    single_url_option = endpoints_config.get(single_endpoint_url, "slug")

    # properties to append to nav menu to attach it to the view class instead
    nav_menu_prop = {"__class": view.__name__, "__module": view.__module__}

    view_name = view.__name__

    Post = model.Cms.Post

    class Postpage(object):

        @classmethod
        def prepare_post(cls, post):
            """
            Prepare the post data,
            """
            url_kwargs = {
                "id": post.id,
                "slug": post.slug,
                "date": post.published_at.strftime("%Y/%m/%d"),
                "month": post.published_at.strftime("%Y/%m")
            }
            # set items not in the accept fields as None to not append in in the url
            url_kwargs = {_: None if _ not in single_url_option["accept"] else __
                          for _, __ in url_kwargs.items()}

            url = url_for("%s:%s" % (view_name, single_endpoint_url),
                          _external=True,
                          **url_kwargs)
            post.url = url
            post.author = cls.prepare_author(post.author)
            return post

        @classmethod
        def prepare_author(cls, author):
            """
            Prepare the author data
            """
            name = utils.slugify(author.name or "no-name")
            url = url_for("%s:post_author" % view_name, id=author.id, name=name, _external=True)
            author.url = url
            return author

        @classmethod
        def get_prev_next_post(cls, post, position):
            """
            Return previous or next post based on the current post
            :params post: post object
            :params position:
            """
            position = position.lower()
            if position not in ["prev", "next"]:
                 raise ValueError("Invalid position key. Must be 'prev' or 'next'")

            posts = Post.get_published(types=post_types)

            if position == "prev":
                posts = posts.filter(Post.id < post.id)
            elif position == "next":
                posts = posts.filter(Post.id > post.id)
            post = posts.first()
            return cls.prepare_post(post) if post else None

        @nav_menu(opt_endpoints.get("index.menu", "All Post"),
                  show=opt_endpoints.get("index.show_menu", True),
                  order=opt_endpoints.get("index.menu_order", 90),
                  **nav_menu_prop)
        @route(opt_endpoints.get("index.endpoint", "posts"))
        def post_index(self):
            """
            Endpoints options:
                index:
                    - menu
                    - show_menu
                    - menu_order
                    - endpoint
                    - per_page
                    - title
                    - post_header
                    - post_subheader
                    - post_show_byline
            """
            page = request.args.get("page", 1)
            app_per_page = self.config("APPLICATION_PAGINATION_PER_PAGE", 10)
            per_page = opt_endpoints.get("index.per_page", app_per_page)

            self.page_meta(title=opt_endpoints.get("index.title", "All Posts"))

            _query = {"types": post_types,
                      "categories": post_categories,
                      "tags": post_tags}

            posts = Post.get_published(**_query).order_by(post_order_by)
            posts = posts.paginate(page=page,
                                   per_page=per_page,
                                   callback=self.prepare_post)
            _kwargs = {
                "post_header": opt_endpoints.get("index.post_header", None),
                "post_subheader": opt_endpoints.get("index.post_subheader", None),
                "post_show_byline": opt_endpoints.get("index.post_show_byline", True)
            }

            return self.render(posts=posts,
                               view_template="%s/post_index.html" % templates_dir,
                               **_kwargs)

        @nav_menu("Post", show=False, **nav_menu_prop)  # No need to show the read in the menu
        @route("%s/<int:id>" % single_endpoint, endpoint="%s:%s" % (view_name, "id"))  # %id
        @route("%s/<slug>" % single_endpoint, endpoint="%s:%s" % (view_name, "slug"))    # %slug
        @route("%s/<int:id>/<slug>" % single_endpoint, endpoint="%s:%s" % (view_name, "id-slug")) # %id-slug
        @route('%s/<regex("[0-9]{4}/[0-9]{2}"):month>/<slug>' % single_endpoint, endpoint="%s:%s" % (view_name, "month-slug")) # %month/slug
        @route('%s/<regex("[0-9]{4}/[0-9]{2}/[0-9]{2}"):date>/<slug>' % single_endpoint, endpoint="%s:%s" % (view_name, "date-slug")) # %date/slug
        def post_single(self, id=None, slug=None, month=None, date=None):
            """
            Endpoints options
                single
                    - post_show_byline
            """
            post = None
            if id:
                post = Post.get_published(id=id, types=post_types)
            elif slug:
                post = Post.get_published(slug=slug, types=post_types)
            if not post:
                abort(404, "Post doesn't exist")

            self.page_meta(title=post.title,
                           image=post.top_image,
                           description=post.excerpt)
            _kwargs = {
                "post_show_byline": opt_endpoints.get("single.post_show_byline", True)
            }
            return self.render(post=self.prepare_post(post),
                               prev_post=self.get_prev_next_post(post, "prev"),
                               next_post=self.get_prev_next_post(post, "next"),
                               view_template="%s/post_single.html" % templates_dir,
                               **_kwargs)

        @nav_menu(opt_endpoints.get("authors.menu", "Authors"),
                  show=opt_endpoints.get("authors.show_menu", False),
                  order=opt_endpoints.get("authors.menu_order", 91),
                  **nav_menu_prop)
        @route(opt_endpoints.get("authors.endpoint", "authors"))
        def post_authors(self):
            """
            Endpoints options
                - authors
                    menu
                    show_menu
                    menu_order
                    endpoint
                    title
            """

            self.page_meta(title=opt_endpoints.get("authors.title", "Authors"))

            authors = []
            return self.render(authors=authors,
                               view_template="%s/post_authors.html" % templates_dir)

        @nav_menu(opt_endpoints.get("author.menu", "Author"),
                  show=False,
                  **nav_menu_prop)
        @route("%s/<id>/<name>" % opt_endpoints.get("author.endpoint", "author"))
        def post_author(self, id, name=None):
            """
            Endpoints options
                - author
                    endpoint
            """

            self.page_meta(title=opt_endpoints.get("author.title", "Author"))

            author = []
            return self.render(author=author,
                               view_template="%s/post_author.html" % templates_dir)

        @nav_menu(opt_endpoints.get("archive.menu", "Archive"),
                  show=opt_endpoints.get("archive.show_menu", False),
                  order=92,
                  **nav_menu_prop)
        @route(opt_endpoints.get("archive.endpoint", "archive"))
        def post_archive(self):
            """
            Endpoints options
                - archive
                    menu
                    show_menu
                    menu_order
                    endpoint
                    title
            """
            self.page_meta(title=opt_endpoints.get("archive.title", "Archive"))

            _query = {"types": post_types,
                      "categories": post_categories,
                      "tags": post_tags}

            posts = Post.get_published(**_query)\
                .order_by(Post.published_at.desc())\
                .group_by(model.db.func.year(Post.published_at),
                          model.db.func.month(Post.published_at))

            return self.render(posts=posts,
                               view_template="%s/post_archive.html" % templates_dir)

    return Postpage

# ------------------------------------------------------------------------------

def admin(view, **kwargs):

    route_base = "cms-admin"
    menu_name = "CMS Admin"

    model = kwargs.get("model")
    templates_dir = kwargs.get("templates_dir", "WebPortfolio/Module/Cms/Admin")
    template_page = templates_dir + "/%s.html"
    PostModel = model.Cms

    # Create a CMS Admin menu for all the methods in Admin
    @nav_menu(menu_name, group="admin")
    class NavMenu(object): pass
    # The nav_menu_context helps attach all the methods to NavMenu
    nav_menu_context = dict(__module=NavMenu.__module__,
                            __class=NavMenu.__name__)
    
    class Admin(object):

        decorators = view.decorators + [login_required]

        @nav_menu("Posts", endpoint="CmsAdmin:index", order=1, **nav_menu_context)
        @route("%s" % route_base, endpoint="CmsAdmin:index")
        def cms_admin_index(self):
            """
            List all posts
            """
            self.page_meta(title="All Posts")
            per_page = self.config("APPLICATION_PAGINATION_PER_PAGE", 25)
            page = request.args.get("page", 1)
            id = request.args.get("id", None)
            slug = request.args.get("slug", None)
            status = request.args.get("status", "all")
            user_id = request.args.get("user_id", None)
            type_id = request.args.get("type_id", None)
            category_id = request.args.get("category_id", None)
            tag_id = request.args.get("tag_id", None)

            reorder_post = request.args.get("reorder_post")

            posts = PostModel.Post.all()
            types = PostModel.Type.all().order_by("name asc")

            selected_type = None
            if type_id:
                selected_type = PostModel.Type.get(type_id)

            if id:
                posts = posts.filter(PostModel.Post.id == id)
            if slug:
                posts = posts.filter(PostModel.Post.slug == slug)
            if user_id:
                posts = posts.filter(PostModel.Post.user_id == user_id)
            if type_id:
                type_id = int(type_id)
                posts = posts.filter(PostModel.Post.type_id == type_id)
            if category_id:
                posts = posts.join(PostModel.CategoryMap)\
                    .join(PostModel.Category)\
                    .filter(PostModel.Category.id == category_id)
            if tag_id:
                posts = posts.join(PostModel.TagMap)\
                    .join(PostModel.Tag)\
                    .filter(PostModel.Tag.id == tag_id)
            if status == "publish":
                posts = posts.filter(PostModel.Post.is_published == True)
            elif status == "draft":
                posts = posts.filter(PostModel.Post.is_draft == True)
            elif status == "revision":
                posts = posts.filter(PostModel.Post.is_revision == True)

            posts = posts.order_by(PostModel.Post.id.desc())
            posts = posts.paginate(page=page, per_page=per_page)

            return self.render(posts=posts,
                               types=types,
                               search=False,
                               query_vars={
                                   "id": id,
                                   "slug": slug,
                                   "user_id": user_id,
                                   "type_id": type_id,
                                   "status": status
                               },
                               selected_type=selected_type,
                               view_template=template_page % "index")

        @nav_menu("Post Preview", endpoint="CmsAdmin:preview", show=False, order=1, **nav_menu_context)
        @route("%s/preview/<id>" % route_base, endpoint="CmsAdmin:preview")
        def cms_admin_preview(self, id):
            """
            Read Post
            """
            post = PostModel.Post.get(id)
            if not post:
                abort(404, "Post doesn't exist")

            self.page_meta(title="Read: %s " % post.title)

            return self.render(post=post,
                               view_template=template_page % "preview")

        @nav_menu("Edit Post", endpoint="CmsAdmin:edit", show=False, **nav_menu_context)
        @nav_menu("New Post", endpoint="CmsAdmin:new", order=2, **nav_menu_context)
        @route("%s/new" % route_base, defaults={"id": None}, endpoint="CmsAdmin:new")
        @route("%s/edit/<id>" % route_base, endpoint="CmsAdmin:edit")
        def cms_admin_edit(self, id):
            """
            Create / Edit Post
            """
            self.page_meta(title="Edit Post")

            types = [(t.id, t.name) for t in PostModel.Type.all().order_by(PostModel.Type.name.asc())]
            categories = [(c.id, c.name) for c in PostModel.Category.all().order_by(PostModel.Category.name.asc())]
            checked_cats = []

            type_id = request.args.get("type_id", None)

            # data to pass to view
            post = {
                "id": 0,
                "title": "",
                "content": "",
                "slug": "",
                "is_public": True,
                "is_sticky": False,
                "is_featured": False,
                "type_id": 0 if not type_id else int(type_id),
                "options": {}
            }

            # saved in session
            flashed_data = get_flashed_data()
            if request.args.get("error") and flashed_data:
                post = flashed_data
                checked_cats = post["post_categories"]

            elif id:
                post = PostModel.Post.get(id)
                if not post or post.is_revision:
                    abort(404, "Post doesn't exist")
                checked_cats = [c.id for c in post.categories]

            images = PostModel.UploadObject.all()\
                .filter(PostModel.UploadObject.type == "IMAGE")\
                .order_by(PostModel.UploadObject.name.asc())

            images_list = [{"id": img.id, "url": img.object_url} for img in images]
            return self.render(post=post,
                               types=types,
                               categories=categories,
                               checked_categories=checked_cats,
                               view_template=template_page % "edit",
                               images_list=images_list)

        @route("%s/post" % route_base, methods=["POST"], endpoint="CmsAdmin:post")
        def cms_admin_post(self):
            id = request.form.get("id")
            title = request.form.get("title")
            slug = request.form.get("slug")
            content = request.form.get("content")
            description = request.form.get("description")
            type_id = request.form.get("type_id")
            post_categories = request.form.getlist("post_categories")
            published_date = request.form.get("published_date")
            status = request.form.get("status", "draft")
            is_published = True if status == "publish" else False
            is_draft = True if status == "draft" else False
            is_public = True if request.form.get("is_public") == "y" else False
            is_sticky = True if request.form.get("is_sticky") == "y" else False
            is_featured = True if request.form.get("is_featured") == "y" else False
            featured_image = request.form.get("featured_image")
            featured_embed = request.form.get("featured_embed")
            featured_media_top = request.form.get("featured_media_top", "")
            social_options = request.form.getlist("social_options")
            tags = list(set(request.form.get("tags", "").split(",")))

            now_dt = datetime.datetime.now()
            data = {
                "title": title,
                "content": content,
                "description": description,
                "featured_image": featured_image,
                "featured_embed": featured_embed,
                "featured_media_top": featured_media_top,
                "type_id": type_id,
                "is_sticky": is_sticky,
                "is_featured": is_featured,
                "is_public": is_public
            }

            if status in ["draft", "publish"] and (not title or not type_id):
                if not title:
                    flash_error("Post Title is missing ")
                if not type_id:
                    flash_error("Post type is missing")

                data.update({
                    "published_date": published_date,
                    "post_categories": post_categories,
                    "options": {"social_options": social_options},
                })
                flash_data(data)

                if id:
                    url = url_for("CmsAdmin:edit", id=id, error=1)
                else:
                    url = url_for("CmsAdmin:new", error=1)
                return redirect(url)

            published_date = datetime.datetime.strptime(published_date, "%Y-%m-%d %H:%M:%S") \
                if published_date else now_dt

            if id and status in ["delete", "revision"]:
                post = PostModel.Post.get(id)
                if not post:
                    abort(404, "Post '%s' doesn't exist" % id)

                if status == "delete":
                    post.delete()
                    flash_success("Post deleted successfully!")
                    return redirect(url_for("CmsAdmin:index"))

                elif status == "revision":
                    data.update({
                        "user_id": current_user.id,
                        "parent_id": id,
                        "is_revision": True,
                        "is_draft": False,
                        "is_published": False,
                        "is_public": False
                    })
                    post = PostModel.Post.create(**data)
                    return jsonify({"revision_id": post.id})

            elif status in ["draft", "publish"]:
                data.update({
                    "is_published": is_published,
                    "is_draft": is_draft,
                    "is_revision": False,
                    "is_public": is_public
                })

                if id:
                    post = PostModel.Post.get(id)
                    if not post:
                        abort(404, "Post '%s' doesn't exist" % id)
                    elif post.is_revision:
                        abort(403, "Can't access this post")
                    else:
                        if is_sticky and not post.is_sticky:
                            data["sticky_at"] = now_dt
                        if is_featured and not post.is_featured:
                            data["featured_at"] = now_dt
                        post.update(**data)
                else:
                    data["user_id"] = current_user.id
                    if is_published:
                        data["published_at"] = published_date
                    if is_sticky:
                        data["sticky_at"] = now_dt
                    if is_featured:
                        data["featured_at"] = now_dt
                    post = PostModel.Post.create(**data)

                # prepare tags
                _tags = []
                for tag in tags:
                    tag = tag.strip().lower()
                    _tag = PostModel.Tag.get_by_slug(name=tag)
                    if tag and not _tag:
                        _tag = PostModel.Tag.new(name=tag)
                    if _tag:
                        _tags.append(_tag.id)
                post.update_tags(_tags)

                post.set_slug(slug or title)
                post.update_categories(map(int, post_categories))
                post.set_options("social", social_options)

                if post.is_published and not post.published_at:
                        post.update(published_at=published_date)

                flash_success("Post saved successfully!")

                return redirect(url_for("CmsAdmin:edit", id=post.id))

            else:
                abort(400, "Invalid post status")

        @nav_menu("Categories", endpoint="CmsAdmin:categories", order=3, **nav_menu_context)
        @route("%s/categories" % route_base, methods=["GET", "POST"], endpoint="CmsAdmin:categories")
        def cms_admin_categories(self):
            self.page_meta(title="Post Categories")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                name = request.form.get("name")
                slug = request.form.get("slug", None)
                ajax = request.form.get("ajax", False)
                try:
                    if not id:
                        cat = PostModel.Category.new(name=name, slug=slug)
                        if ajax:
                            return jsonify({
                                "id": cat.id,
                                "name": cat.name,
                                "slug": cat.slug,
                                "status": "OK"
                            })
                        flash_success("New category '%s' added" % name)
                    else:
                        post_cat = PostModel.Category.get(id)
                        if post_cat:
                            if action == "delete":
                                post_cat.delete()
                                flash_success("Category '%s' deleted successfully!" % post_cat.name)
                            else:
                                post_cat.update(name=name, slug=slug)
                                flash_success("Category '%s' updated successfully!" % post_cat.name)
                except Exception as ex:
                    if ajax:
                        return jsonify({
                            "error": True,
                            "error_message": ex.message
                        })

                    flash_error("Error: %s" % ex.message)
                return redirect(url_for("CmsAdmin:categories"))

            else:
                cats = PostModel.Category.all().order_by(PostModel.Category.name.asc())
                return self.render(categories=cats,
                                   view_template=template_page % "categories")

        @nav_menu("Tags", endpoint="CmsAdmin:tags", order=4, **nav_menu_context)
        @route("%s/tags" % route_base, methods=["GET", "POST"], endpoint="CmsAdmin:tags")
        def cms_admin_tags(self):
            self.page_meta(title="Post Tags")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                name = request.form.get("name")
                slug = request.form.get("slug", None)
                ajax = request.form.get("ajax", False)
                try:
                    if not id:
                        tag = PostModel.Tag.new(name=name, slug=slug)
                        if ajax:
                            return jsonify({
                                "id": tag.id,
                                "name": tag.name,
                                "slug": tag.slug,
                                "status": "OK"
                            })
                        flash_success("New Tag '%s' added" % name)
                    else:
                        post_tag = PostModel.Tag.get(id)
                        if post_tag:
                            if action == "delete":
                                post_tag.delete()
                                flash_success("Tag '%s' deleted successfully!" % post_tag.name)
                            else:
                                post_tag.update(name=name, slug=slug)
                                flash_success("Tag '%s' updated successfully!" % post_tag.name)
                except Exception as ex:
                    if ajax:
                        return jsonify({
                            "error": True,
                            "error_message": ex.message
                        })

                    flash_error("Error: %s" % ex.message)
                return redirect(url_for("CmsAdmin:tags"))

            else:
                tags = PostModel.Tag.all().order_by(PostModel.Tag.name.asc())
                return self.render(tags=tags,
                                   view_template=template_page % "tags")

        @nav_menu("Types", endpoint="CmsAdmin:types", order=5, **nav_menu_context)
        @route("%s/types" % route_base, methods=["GET", "POST"], endpoint="CmsAdmin:types")
        def cms_admin_types(self):
            self.page_meta(title="Post Types")
            if request.method == "POST":
                try:
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    name = request.form.get("name")
                    slug = request.form.get("slug", None)
                    if not id:
                        PostModel.Type.new(name=name, slug=slug)
                        flash_success("New type '%s' added" % name)
                    else:
                        post_type = PostModel.Type.get(id)
                        if post_type:
                            if action == "delete":
                                post_type.delete()
                                flash_success("Type '%s' deleted successfully!" % post_type.name)
                            else:
                                post_type.update(name=name, slug=slug)
                                flash_success("Type '%s' updated successfully!" % post_type.name)
                except Exception as ex:
                    flash_error("Error: %s" % ex.message)
                return redirect(url_for("CmsAdmin:types"))
            else:
                types = PostModel.Type.all().order_by(PostModel.Type.name.asc())
                return self.render(types=types,
                                   view_template=template_page % "types")

        @nav_menu("Images", endpoint="CmsAdmin:images", order=6, **nav_menu_context)
        @route("%s/images" % route_base, methods=["GET", "POST"], endpoint="CmsAdmin:images")
        def cms_admin_images(self):
            self.page_meta(title="Images")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                description = request.form.get("description")
                if id:
                    image = PostModel.UploadObject.get(id)
                    if image:
                        if action == "delete":
                            image.delete()
                            obj = storage.get(image.name)
                            if obj:
                                obj.delete()
                            flash_success("Image deleted successfully!")
                        else:
                            image.update(description=description)
                            flash_success("Image updated successfully!")
                else:
                    abort(404, "No image ID provided")
                return redirect(url_for("CmsAdmin:images"))

            else:
                page = request.args.get("page", 1)
                per_page = self.config("PAGINATION_PER_PAGE", 25)
                images = PostModel.UploadObject.all()\
                    .filter(PostModel.UploadObject.type == "IMAGE")\
                    .order_by(PostModel.UploadObject.name.asc())
                images = images.paginate(page=page, per_page=per_page)
                return self.render(images=images,
                                   view_template=template_page % "images")

        @route("%s/upload-image" % route_base, methods=["POST"], endpoint="CmsAdmin:upload_image")
        def cms_admin_upload_image(self):
            """
            Placeholder for markdown
            """
            try:
                ajax = request.form.get("ajax", False)
                allowed_extensions = ["gif", "png", "jpg", "jpeg"]

                if request.files.get("file"):
                    _file = request.files.get('file')
                    obj = storage.upload(_file,
                                         prefix="cms-uploads/",
                                         allowed_extensions=allowed_extensions,
                                         public=True)

                    if obj:
                        description = os.path.basename(obj.name)
                        description = description.replace(".%s" % obj.extension, "")
                        description = description.split("__")[0]
                        upload_object = PostModel.UploadObject.create(name=obj.name,
                                                                      provider=obj.provider_name,
                                                                      container=obj.container.name,
                                                                      extension=obj.extension,
                                                                      type=obj.type,
                                                                      object_path=obj.path,
                                                                      object_url=obj.url,
                                                                      size=obj.size,
                                                                      description=description)
                        if ajax:
                            return jsonify({
                                "id": upload_object.id,
                                "url": upload_object.object_url
                            })
                        else:
                            flash_success("Image '%s' uploaded successfully!" % upload_object.name)

                else:
                    flash_error("Error: Upload object file is invalid or doesn't exist")
            except Exception as e:
                flash_error("Error: %s" % e.message)
            return redirect(url_for("CmsAdmin:images"))

    return Admin
