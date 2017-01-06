"""
This is an AWS Lambda function to handle an Echo skill to pray the rosary
from a local zip file with a library
"""

from __future__ import print_function
from token_data import TokenData
from datetime import date
import calendar
import dateutil.parser


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    print ("Bulding speechlet response")
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Rosary - " + title,
            'content': "Rosary - " + card_text
        },
        'reprompt': {
            'type': 'PlainText',
            'text': reprompt_text
        },
        'directives': [],
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_pray_response():
    print ("Sending response")
    session_attributes = {}
    currentData = TokenData('Rosary','Joyful','Creed',0,0)
    return build_response(session_attributes, {
        'outputSpeech': {
            'type': 'PlainText',
            'text': "Beginning the rosary"
        },
        'card': {
            'type': 'Simple',
            'title': "Rosary - playing",
            'content': "Rosary -  playing"
        },
        'reprompt': {            
        },
        'directives': [
        {
            'type': 'AudioPlayer.ClearQueue',
            'clearBehavior': 'CLEAR_ENQUEUED'
        },
        {
            'type': 'AudioPlayer.Play',
            'playBehavior': 'REPLACE_ALL',
            'audioItem': {
                'stream': {
                    'token': currentData.get_token(),
                    'url': currentData.get_audio(),
                    'offsetInMilliseconds': 0
                }
            }
        }
        ],
        'shouldEndSession': True
    })


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(timestamp):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    
    my_date = dateutil.parser.parse(timestamp)
    day_name = calendar.day_name[my_date.weekday()]
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Today is " + day_name + ". Shall I begin?"
    reprompt_text = "Shall I begin?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, timestamp + " " + speech_output,
        should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response(launch_request["timestamp"])


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Pray":
        return build_pray_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

def on_playback_started(started_request):
    print("Playback started for " + started_request['token'])
    return build_empty_response()


def on_playback_finished(finished_request):
    print("Playback finished for " + finished_request['token'])
    return build_empty_response()


def on_playback_stopped(stopped_request):
    print("Playback stopped for " + stopped_request['token'])
    return build_empty_response()



def build_empty_response():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
        "shouldEndSession": True
        }
    }

def on_playback_nearly_finished(nearly_finished_request):
    print("playing next prayer")
    token = nearly_finished_request['token']
    current_data = TokenData.from_token(token)
    next_data = current_data.get_next()
    if next_data:
        return {
           'version': '1.0',
           'response': {
               'directives': [
                   {
                       'type': 'AudioPlayer.Play',
                       'playBehavior': 'ENQUEUE',
                       'audioItem': {
                           'stream': {
                               'token': next_data.get_token(),
                               'url': next_data.get_audio(),
                               'offsetInMilliseconds': 0,
                               'expectedPreviousToken': token
                           }
                       }
                   }
               ]
           }
       }
    else:
        print ("Finishing")
        return build_empty_response();
   
def on_play_command(play_request, context):
    print("Resuming prayer")
    token = context['AudioPlayer']['token']
    current_data = TokenData.from_token(token)
    return {
        'version': '1.0',
        'response': {
            'directives': [
                {
                    'type': 'AudioPlayer.Play',
                    'playBehavior': 'REPLACE_ALL',
                    'audioItem': {
                        'stream': {
                            'token': current_data.get_token(),
                            'url': current_data.get_audio(),
                            'offsetInMilliseconds': context['AudioPlayer']['offsetInMilliseconds'],
                        }
                    }
                }
            ]
        }
    }
   

def on_playback_failed(request):
    print ("Playback failed: " + request['error']['type']
           + ":" + request['error']['message'])
    return {
        'version': '1.0',
        'response': {
            'directives': [
                {
                    'type': 'AudioPlayer.Stop'
                }
            ]
           }
       }
    


def handle_exception(request):
    print ("Exception encountered: " + request['error']['type']
           + ":" + request['error']['message']
           + " for " + request["cause"]["requestId"])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
#    print("event.session.application.applicationId=" +
#          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

#    if event['session']['new']:
#        on_session_started({'requestId': event['request']['requestId']},
#                           event['session'])

    print("Processing event: " + event['request']['requestId']
          + ": " + event['request']['type']);

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    elif event['request']['type'] == "AudioPlayer.PlaybackNearlyFinished":
        return on_playback_nearly_finished(event['request'])
    elif event['request']['type'] == "AudioPlayer.PlaybackStarted":
        return on_playback_started(event['request'])
    elif event['request']['type'] == "AudioPlayer.PlaybackFinished":
        return on_playback_finished(event['request'])
    elif event['request']['type'] == "AudioPlayer.PlaybackStopped":
        return on_playback_stopped(event['request'])
    elif event['request']['type'] == "AudioPlayer.PlaybackStopped":
        return on_playback_stopped(event['request'])
    elif event['request']['type'] == "AudioPlayer.PlaybackFailed":
        return on_playback_failed(event['request'])
    elif event['request']['type'] == "PlaybackController.PlayCommandIssued":
        return on_play_command(event['request'], event['context'])
    elif event['request']['type'] == "System.ExceptionEncountered":
        handle_exception(event['request'])

