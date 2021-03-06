#######################################################################
#######################################################################
### To Print the Guest List Dictionary:                             ###
###     @command line type:  python meetings.py                     ###
### To Send Emails:                                                 ###
###     add the -e or --email flag                                  ###
###     @command line type:  python meetings.py -e                  ###
#######################################################################
#######################################################################
import requests
from pprint import pprint
from datetime import datetime, timedelta
import collections

class MeetingMaker():
    _url ="https://ct-api-challenge.herokuapp.com/"
    _json = None
    _country_list=[]
    _people=[]
    _avail_dates={}
    _best_date_dict = {}
    _attendees = {}
    _meeting_dict_list=[]

    @classmethod
    def _make_json(cls):
        cls._json=requests.get(cls._url).json()

    @classmethod
    def _find_countries(cls):
        for partner in cls._json['partners']:
            if partner['country'] not in cls._country_list:
                cls._country_list.append(partner['country'])

    @classmethod
    def _partner_info(cls):
        for partner in cls._json['partners']:
            cls._people.append({'email': partner["email"],'dates': partner["availableDates"],'country': partner['country']})
    
    @classmethod
    def _find_all_availible_dates_by_country(cls):
        
        for country in cls._country_list:
            cls._avail_dates[country] = []
        for people in cls._people:
            for i in range(len(people['dates'])):
                people['dates'][i] = datetime.strptime(people['dates'][i], '%Y-%m-%d').date()
            for i in range(len(people['dates'])):
                if people['dates'][i] + timedelta(days=1) in people['dates']:
                    cls._avail_dates[people['country']].append(people['dates'][i])

    @classmethod
    def _find_best_dates(cls):
        for country, datelist in cls._avail_dates.items():
            ctr=collections.Counter(datelist)
            maxc=max(ctr.values())
            bsd=[]
            for k, v in ctr.items():
                if v == maxc:
                    bsd.append(k)
            cls._best_date_dict.update({country:bsd[0]})
            
    @classmethod
    def _find_attendees(cls):
        for country in cls._country_list:
            cls._attendees[country] = []
        for country, date in cls._best_date_dict.items():
            for people in cls._people:
                if date in people["dates"] and country in people["country"]:   
                    cls._attendees[country].append(people['email'])

    @classmethod 
    def _make_meeting_dict_list(cls):
        for country in cls._country_list:
            sd=''
            a=[]
            ct=0
            for c, d in cls._best_date_dict.items():
                if country == c:
                    sd = d.strftime('%Y-%m-%d')
            for c, ad in cls._attendees.items():
                if country == c:
                    a=ad
                    ct=len(a)
            tempdict={
                'attendeeCount' : ct,
                'attendees' : a,
                'startDate' : sd,
                'name' : country}
            cls._meeting_dict_list.append(tempdict)

    @classmethod
    def _display(cls):
        pprint(cls._meeting_dict_list)
        
    @classmethod
    def return_dict(cls):
        MeetingMaker._make_json()
        MeetingMaker._find_countries()
        MeetingMaker._partner_info()
        MeetingMaker._find_all_availible_dates_by_country()
        MeetingMaker._find_best_dates()
        MeetingMaker._find_attendees()
        MeetingMaker._make_meeting_dict_list()
        return(cls._meeting_dict_list)

    @staticmethod
    def _main():        
        MeetingMaker._make_json()
        MeetingMaker._find_countries()
        MeetingMaker._partner_info()
        MeetingMaker._find_all_availible_dates_by_country()
        MeetingMaker._find_best_dates()
        MeetingMaker._find_attendees()
        MeetingMaker._make_meeting_dict_list()
        MeetingMaker._display()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "-e", "--email", dest="sendEmail", help="This will send out the invitations", action='store_true')
    args = parser.parse_args()

    if args.sendEmail:
        import emailer
    else:
        MeetingMaker._main()



