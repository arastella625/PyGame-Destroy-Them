import os
import sys
import unittest

# Force SDL to use dummy video driver before pygame is imported
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

# Run unittest discovery from the tests folder
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(__file__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # mirror exit code behavior for CI
    sys.exit(result.wasSuccessful())