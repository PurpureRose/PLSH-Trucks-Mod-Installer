try:
    import pip
    pip.main(['install', 'ttkbootstrap', 'requests', 'gdown'])
except ImportError:
    print("pip is not available. Please install it manually.")
except Exception as e:
    print(f"Error installing libraries: {e}")
