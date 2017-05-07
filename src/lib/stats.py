#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

def stats():
	cmd = "echo \"CPU stats:\\n#############\"; top -bn1 -o%CPU |head -12|tail -6|awk \'{ printf(\"%-8s %-8s %-8s %-8s %-8s\\n\", $1, $2, $9, $10, $12); }\';echo \"\\nRAM stats:\\n#############\";echo \"(MB) \\t\\t Total \\t\\t Used \\t\\t Free\";free -m|head -2|tail -1|awk \'{ printf(\"%-8s %-8s %-8s %-8s\\n\", $1, $2, $3, $4); }\';echo \"\\nHDD stats:\\n#############\";df -h;echo \"\\nOther stats:\\n#############\";/opt/vc/bin/vcgencmd measure_temp|sed \'s/temp=/Temperature: /g\'|sed \"s/\'/º/g\";uptime -p|sed -e \'s/\\(.*\\)/Uptime: \\1/g\'"
	return os.popen(cmd).read()