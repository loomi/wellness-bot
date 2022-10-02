from dotenv import load_dotenv

from main.application import Application

if __name__ == "__main__":
    load_dotenv()

    app = Application()

    app.run()
