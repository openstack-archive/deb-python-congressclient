#   Copyright 2012-2013 OpenStack, LLC.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""Policy action implemenations"""

import logging

from cliff import command
from cliff import lister
from cliff import show
import six

from congressclient.common import utils
from congressclient.openstack.common import jsonutils


def _format_rule(rule):
    """Break up rule string so it fits on screen."""

    rule_split = jsonutils.dumps(rule).split(":-")
    formatted_string = rule_split[0] + ":-\n"
    for rule in rule_split[1].split("), "):
        formatted_string += rule + '\n'
    return formatted_string


class CreatePolicyRule(show.ShowOne):
    """Create a policy rule."""

    log = logging.getLogger(__name__ + '.CreatePolicyRule')

    def get_parser(self, prog_name):
        parser = super(CreatePolicyRule, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name or identifier of the policy")
        parser.add_argument(
            'rule',
            metavar="<rule>",
            help="Policy rule")

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        body = {'rule': parsed_args.rule}
        data = client.create_policy_rule(parsed_args.policy_name, body)
        data['rule'] = _format_rule(data['rule'])
        return zip(*sorted(six.iteritems(data)))


class DeletePolicyRule(command.Command):
    """Delete a policy rule."""

    log = logging.getLogger(__name__ + '.DeletePolicyRule')

    def get_parser(self, prog_name):
        parser = super(DeletePolicyRule, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy to delete")
        parser.add_argument(
            'rule_id',
            metavar="<rule-id>",
            help="ID of the policy to delete")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        client.delete_policy_rule(parsed_args.policy_name,
                                  parsed_args.rule_id)


class ListPolicyRules(lister.Lister):
    """List policy rules."""

    log = logging.getLogger(__name__ + '.ListPolicyRules')

    def get_parser(self, prog_name):
        parser = super(ListPolicyRules, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        data = client.list_policy_rules(parsed_args.policy_name)['results']
        columns = ['id', 'comment', 'rule']
        formatters = {'PolicyRules': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class ListPolicy(lister.Lister):
    """List Policy."""

    log = logging.getLogger(__name__ + '.ListPolicy')

    def get_parser(self, prog_name):
        parser = super(ListPolicy, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.congressclient
        data = client.list_policy()['results']
        columns = ['id', 'owner_id']
        formatters = {'Policies': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))


class GetPolicyRow(lister.Lister):
    """Get policy row."""

    log = logging.getLogger(__name__ + '.GetPolicyRow')

    def get_parser(self, prog_name):
        parser = super(GetPolicyRow, self).get_parser(prog_name)
        parser.add_argument(
            'policy_name',
            metavar="<policy-name>",
            help="Name of the policy to show")
        parser.add_argument(
            'table',
            metavar="<table>",
            help="Table to get the policy row from")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        client = self.app.client_manager.congressclient
        data = client.get_policy_rows(parsed_args.policy_name,
                                      parsed_args.table)['results']

        columns = ['data']
        formatters = {'Policies': utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns,
                                           formatters=formatters)
                 for s in data))
