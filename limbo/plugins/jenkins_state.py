"""!build: show last build state"""

import re
from jenkinsapi.jenkins import Jenkins
from limbo import conf

JENKINS_URL = 'https://jenkins.adnxs.net/'
OPT_KEY = 'OPT-Optimization-Tests'

username = conf.appnexus_user
password = conf.appnexus_pass


def on_message(msg, server):
    body = msg.get("text", "")
    reg = re.compile('(!build)', re.IGNORECASE)
    match = reg.match(body)
    if not match:
        return
    J = Jenkins(JENKINS_URL, username=username, password=password)
    JOPT = J[OPT_KEY]
    last = JOPT.get_last_build()
    response = 'State: ' + (last.get_status() or 'Building') + '\n'
    response += 'Build number: ' + str(last.get_number()) + '\n'
    response += 'Built time: ' + last.get_timestamp().strftime('%Y-%m-%d %H:%M:%S') + '\n'
    response += last.get_result_url()[:-10]
    if last.get_status() == "SUCCESS":
        response += '\nhttp://i.imgur.com/ikXlak4.gif'
    else:
        response += '\nhttp://i.imgur.com/7T2ANEO.gif'
    return response
