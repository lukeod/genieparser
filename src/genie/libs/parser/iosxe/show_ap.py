import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# ===============================
# Schema for:
#  * 'show ap rf-profile summary'
# ===============================
class ShowApRfProfileSummarySchema(MetaParser):
    """Schema for show ap rf-profile summary."""

    schema = {
        "rf_profile_summary": {
            "rf_profile_count": int,
            "rf_profiles": {
                str: {
                    "rf_profile_name": str,
                    "band": str,
                    "description": str,
                    "state": str
                }
            }
        }
    }


# ===============================
# Parser for:
#  * 'show ap rf-profile summary'
# ===============================
class ShowApRfProfileSummary(ShowApRfProfileSummarySchema):
    """Parser for show ap rf-profile summary"""

    cli_command = 'show ap rf-profile summary'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        rf_profile_summary_dict = {}

        # Number of RF-profiles: 14
        #
        # RF Profile Name                  Band     Description                          State
        # ------------------------------------------------------------------------------------
        # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
        # Custom-RF_b                      2.4 GHz  Custom-RF_b_Desc                     Up
        # Low_Client_Density_rf_5gh        5 GHz    pre configured Low Client Density rf Up
        # High_Client_Density_rf_5gh       5 GHz    pre configured High Client Density r Up
        # Low-Client-Density-802.11a       5 GHz                                         Up
        # Low_Client_Density_rf_24gh       2.4 GHz  pre configured Low Client Density rf Up
        # High-Client-Density-802.11a      5 GHz                                         Up
        # High_Client_Density_rf_24gh      2.4 GHz  pre configured High Client Density r Up
        # Low-Client-Density-802.11bg      2.4 GHz                                       Up
        # High-Client-Density-802.11bg     2.4 GHz                                       Up
        # Typical_Client_Density_rf_5gh    5 GHz    pre configured Typical Density rfpro Up
        # Typical-Client-Density-802.11a   5 GHz                                         Up
        # Typical_Client_Density_rf_24gh   2.4 GHz  pre configured Typical Client Densit Up
        # Typical-Client-Density-802.11bg  2.4 GHz                                       Up
        #


        # Number of RF-profiles: 14
        rf_profile_count_capture = re.compile(r"^Number\s+of\s+RF-profiles:\s+(?P<rf_profile_count>\d+)")
        # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
        rf_profile_info_capture = re.compile(
            r"^(?P<rf_profile_name>\S+)\s+(?P<band>\S+\s+\S+)\s+(?P<description>.*)(?P<state>(Up|Down))")
        # RF Profile Name                  Band     Description                          State
        # ------------------------------------------------------------------------------------


        rf_profile_data = {}

        for line in out.splitlines():
            line = line.strip()
            # Number of RF-profiles: 14
            if rf_profile_count_capture.match(line):
                rf_profile_count_match = rf_profile_count_capture.match(line)
                groups = rf_profile_count_match.groupdict()
                rf_profile_count = int(groups['rf_profile_count'])
                if not rf_profile_summary_dict.get('rf_profile_summary', {}):
                    rf_profile_summary_dict['rf_profile_summary'] = {}
                rf_profile_summary_dict['rf_profile_summary']['rf_profile_count'] = rf_profile_count
                continue
            elif line.startswith('RF Profile Name'):
                continue
            elif line.startswith('-----'):
                continue
            # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
            elif rf_profile_info_capture.match(line):
                rf_profile_info_match = rf_profile_info_capture.match(line)
                groups = rf_profile_info_match.groupdict()
                rf_profile_name = ''
                for k, v in groups.items():
                    if k == 'rf_profile_name':
                        rf_profile_name = v
                    v = v.strip()
                    if not rf_profile_summary_dict['rf_profile_summary'].get('rf_profiles', {}):
                           rf_profile_summary_dict['rf_profile_summary']['rf_profiles'] = {}
                    rf_profile_summary_dict['rf_profile_summary']['rf_profiles'][rf_profile_name] = {}
                    rf_profile_data.update({k: v})
                rf_profile_summary_dict['rf_profile_summary']['rf_profiles'][rf_profile_name].update(rf_profile_data)
                rf_profile_data = {}
                continue

        return rf_profile_summary_dict
