import http.client
import pandas as pd
import numpy as np
from .common import *
from .exceptions import *

def get_hs_info(username):
    try:
        conn = http.client.HTTPSConnection('secure.runescape.com')
        conn.request('GET', '/m=hiscore_oldschool/index_lite.ws?player={}'.format(username))
    except:
        raise BadRequestException()

    r = conn.getresponse()
    if r.status == http.client.NOT_FOUND:
        raise BadRsnException()

    data = r.read().decode()
    temp_data = list(filter(None, data.split('\n')))
    stat_hs = temp_data[:len(skill_names)]
    activity_hs = temp_data[len(skill_names):len(skill_names)+len(activity_names)]
    boss_hs = temp_data[-(len(boss_names)):]

    stats = []
    for skill in stat_hs:
        stats.append(skill.split(','))
    stats_df = pd.DataFrame(stats, index=skill_names, columns=skill_columns).replace('-1', 'unranked')

    activities = []
    for activity in activity_hs:
        activities.append(activity.split(','))
    activities_df = pd.DataFrame(activities, index=activity_names, columns=activity_columns).replace('-1', 'unranked')

    bosses = []
    for boss in boss_hs:
        bosses.append(boss.split(','))
    bosses_df = pd.DataFrame(bosses, index=boss_names, columns=boss_columns).replace('-1', 'unranked')

    hs_data = {
        'skills': stats_df,
        'activities': activities_df,
        'bosses': bosses_df
    }

    return hs_data


def main():
    hs_data = get_hs_info('RexMorganMD')

if __name__ == '__main__':
    main()