from itsdangerous import URLSafeTimeSerializer

from .. import app

ts = URLSageTimeSerializer(app.config["SECRET.KEY"])
