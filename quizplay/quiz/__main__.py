from quiz import create_app


def main():
    # debug mode for local
    app = create_app()
    app.app.debug = True
    # app.app.run(host=app.app.config['HOST'], port=app.app.config['PORT'], debug=True)
    app.run(port=8081)


if __name__ == "__main__":
    main()
