#!/bin/env python3

# Copyright (C) Maciej Suminski <orson@orson.net.pl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you may find one here:
# https://www.gnu.org/licenses/gpl-3.0.html
# or you may search the http://www.gnu.org website for the version 3 license,
# or you may write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import os
from flask import Flask, request, abort
import json
import gitlab

gitlab_url = os.environ['GITLAB_URL']
gitlab_token = os.environ['GITLAB_API_TOKEN']
gitlab_secret = os.environ['GITLAB_SECRET']

app = Flask(__name__)

@app.route('/issue', methods=['POST'])
def issue():
    try:
        if request.headers['X-Gitlab-Token'] != gitlab_secret:
            abort(403)

        if request.headers['X-Gitlab-Event'] != 'Issue Hook':
            abort(400)

        payload = json.loads(request.data)
        gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
        project = gl.projects.get(payload['project']['id'])

        issue = project.issues.get(payload['object_attributes']['iid'])
        issue.labels.append('priority::undecided')
        issue.labels.append('status::new')
        issue.save()

        return 'OK'
    except:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
