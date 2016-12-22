# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.api import neutron

LOG = logging.getLogger(__name__)


class Firewall(horizon.Panel):
    name = _("Firewalls")
    slug = "firewalls"
    permissions = ('openstack.services.network',)
    policy_rules = (("network", "get_firewall"),)

    def allowed(self, context):
        request = context['request']
        if not request.user.has_perms(self.permissions):
            return False
        try:
            if not neutron.is_service_enabled(request,
                                              config_name='enable_firewall',
                                              ext_name='fwaas'):
                return False
        except Exception:
            LOG.error("Call to list enabled services failed. This is likely "
                      "due to a problem communicating with the Neutron "
                      "endpoint. Firewalls panel will not be displayed.")
            return False
        if not super(Firewall, self).allowed(context):
            return False
        return True
