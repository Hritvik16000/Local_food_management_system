import os
import sys
import streamlit as st

st.write("Current working dir:", os.getcwd())
st.write("Python version:", sys.version)
st.write("Installed packages:")

import pkg_resources
installed = sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])
st.write(installed)

from sqlalchemy import create_engine
st.write("SQLAlchemy imported successfully!")

