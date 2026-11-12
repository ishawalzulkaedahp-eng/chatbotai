from backend.server import run

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")