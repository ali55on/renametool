#!/usr/bin/env python3
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

import frontend.ui


ui = frontend.ui.ChangeUi()
ui.main()
