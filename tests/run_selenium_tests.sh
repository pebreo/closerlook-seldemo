#trap 'rm -rf PBTESTENV' EXIT  # Clean virtualenv dir on exit
#virtualenv PBTESTENV
#source PBTESTENV/bin/activate
pip install -r sel_requirements.txt

export ENABLE_XVFB=1    # run the tests headless using Xvfb. Set 0 to disable
chromium-browser --version
py.test -s selenium  # autodiscover and run the tests

