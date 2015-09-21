from . import decorator
from . import filehandlers
from . import configuration 
from . import articles
from . import preprocessor
import jinja2
import os
import markdown
import logging

def make_sure_dir_exists(folder_path):
    dir = os.path.dirname(folder_path)
    if not os.path.exists(dir):
        logging.info("Creating directory: %s", dir)
        try:
            os.makedirs(dir)
        except:
            logging.warning("Cannot create directory: %s", dir)

def make_embedded_articles(template):
    r = {}
    if template.embedd != None:
        for variable_name, article in template.embedd.items():
            logging.info("Embedding article: %s", article)
            r[variable_name] = markdown.markdown(articles.get_article_from(configuration['source'], article).content)
    return r

def generate(source, output, decorator_path, templates_folder, template_map):
    d = decorator.Decorator(decorator_path, templates_folder, template_map)
    d.add_handler('.less', filehandlers.LessProcessor)
    d.build_decoration(output)
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(d.template_folder))
    for article in articles.get_articles_from(source):
        template = d.get_template_for_type(article.type)
        if template == None:
            logging.warning("No template found for article type: %s", article.type)
            continue
        jinja_template = environment.get_template(template.file)
        if article.permalink != None:
            output_path = os.path.join(output, article.permalink)
            if article.publish:
                make_sure_dir_exists(output_path)
                md_content = preprocessor.process(article.content, article.name)
                content = markdown.markdown(md_content, extensions=['markdown.extensions.toc', 'markdown.extensions.fenced_code'])
                data = article.data
                data.update(make_embedded_articles(template))
                with open(output_path, 'wb') as f:
                    f.write(jinja_template.render(content=content, **data).encode("utf-8"))
                logging.info("File written: %s", output_path)
            else:
                logging.info("Not publishing %s",  article.name)
                try:
                    os.remove(output_path)
                except:
                    pass

def main():
    try:
        config = configuration.read()
        generate(config['source'], config['output'], config['decorator'], config['template'], config['templatemap'])
        logging.info("Successfully created site in %s", config['output'])
    except Exception as ex:
        logging.error(str(ex))
        raise
