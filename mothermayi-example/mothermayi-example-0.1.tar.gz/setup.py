from setuptools import setup

def main():
    setup(
        name                 = "mothermayi-example",
        version              = "0.1",
        description          = "An example plugin for mothermayi",
        url                  = "https://github.com/EliRibble/mothermayi-example",
        long_description     = "An example plugin for mothermayi",
        author               = "Eli Ribble",
        author_email         = "junk@theribbles.org",
        install_requires    = [
            'mothermayi',
        ],
        packages             = ["mmiexample"],
        package_data         = {
            "mmiexample"     : ["mmiexample/*"],
        },
        entry_points = {
            'mothermayi' : [
                'plugin = mmiexample.main:plugin',
            ]
        },
        include_package_data = True,
    )

if __name__ == "__main__":
    main()
