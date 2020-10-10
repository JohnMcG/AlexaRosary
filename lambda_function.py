"""
This is an AWS Lambda function to handle an Echo skill to pray the rosary
from a local zip file with a library

by John McGuinness, 2017
"""

from __future__ import print_function
from token_data import TokenData
from token_data import RosaryTokenData
from token_data import DivineMercyTokenData


DAYS_OF_WEEK = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
MYSTERIES = ['joyful','sorrowful','glorious','luminous']

MYSTERIES_MAP = {
    'sunday' : 'glorious',
    'monday' : 'joyful',
    'tuesday' : 'sorrowful',
    'wednesday' : 'glorious',
    'thursday' : 'luminous',
    'friday' : 'sorrowful',
    'saturday' : 'joyful'
    }

SMALL_IMAGE_URL='https://s3.amazonaws.com/rosary-files/img/rosary_small.jpg'
LARGE_IMAGE_URL='https://s3.amazonaws.com/rosary-files/img/rosary_large.jpg'
IMAGE_CREDIT = 'By FotoKatolik from Polska (Rozaniec) [CC BY-SA 2.0 (http://creativecommons.org/licenses/by-sa/2.0)], via Wikimedia Commons\r\n\r\n'
HELP_TEXT = 'You can say Divine Mercy Chaplet, Rosary, or request the Joyful, Sorrowful, Glorious, or Luminous Mysteries.' 
HELP_REPROMPT = 'What would you like me to pray with you?'
DEFAULT_MYSTERIES_SLOTS = { 'mysteries': ''}
DEFAULT_DAY_SLOTS = {'day' : {'value': ''}}
DEFAULT_VALUES = {'value' : '' }
DEFAULT_VALUE = ''
APP_TITLE = 'Prayer Buddy'

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session, directives):
    print ("Bulding speechlet response")
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': 'Prayer Buddy - ' + title,
            'text': IMAGE_CREDIT + APP_TITLE + ' - ' + card_text,
            'image' : {
                'smallImageUrl': SMALL_IMAGE_URL,
                'largeImageUrl': LARGE_IMAGE_URL
            }

        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'directives': directives,
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def get_farewell_response():
    directives = [
                {
                    'type': 'AudioPlayer.Stop'
                }
            ] 
    return build_response({}, build_speechlet_response(
        APP_TITLE, 'goodbye', '', 'goodbye',
        True, directives))

def get_help_response():
    return build_response({}, build_speechlet_response(
        APP_TITLE, HELP_TEXT + " " + HELP_REPROMPT, HELP_REPROMPT, HELP_TEXT, False, []))

def not_supported():
    return build_response({}, build_speechlet_response(
        'Rosary', 'Operation not supported', '', 'Operation not supported',
        True, []))

def bad_day_of_week_input(day, dialogState):
    directives = []
    if dialogState != 'UNDEFINED':
        directives = [{
                    'type': 'Dialog.ElicitSlot',
                    'slotToElicit': 'day'
                }]
    message = day + ' is not a day of the week. Please say a day of the week.'
    return build_response({}, build_speechlet_response(
        APP_TITLE, message, message, message, False, directives))

def bad_mysteries_input(mysteries, dialogState):    
    directives = []
    if dialogState != 'UNDEFINED':
        directives = [{
                    'type': 'Dialog.ElicitSlot',
                    'slotToElicit': 'mysteries'
                }]
    message = mysteries + (" is not a set of mysteries of the Rosary. " 
                           "Please say Joyful, Sorrowful, Glorious, or Luminous.")
    return build_response({}, build_speechlet_response(
        APP_TITLE, message, message, message, False, directives))
                          

def start_over(token):
    current_data = TokenData.from_token(token)
    if current_data.prayer_type == 'Rosary':
        return build_pray_response(current_data.mysteries)
    else:
        return build_divine_mercy_response()
       

def build_pray_response(mysteries):
    print ("Sending response for " + mysteries + " mysteries.")
    session_attributes = {}
    currentData = RosaryTokenData(mysteries,'SignOfTheCross',0,0)
    return build_response(session_attributes, {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Beginning the ' + mysteries.capitalize() + ' mysteries of the rosary'
        },
        'card': {
            'type': 'Standard',
            'title': mysteries.capitalize() + ' mysteries of the Rosary',
            'text':  IMAGE_CREDIT + mysteries.capitalize() + ' mysteries of the Rosary',
            'image' : {
                'smallImageUrl': SMALL_IMAGE_URL,
                'largeImageUrl': LARGE_IMAGE_URL
            }
        },
        'reprompt': {            
        },
        'directives': [
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


def build_divine_mercy_response():
    print ("Sending response for chaplet of divine mercy")
    session_attributes = {}
    currentData = DivineMercyTokenData('SignOfTheCross',0,0)
    return build_response(session_attributes, {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Beginning the Divine Mercy Chaplet'
        },
        'card': {
            'type': 'Standard',
            'title': 'Divine Mercy Chaplet',
            'text':  IMAGE_CREDIT + ' Divine Mercy Chaplet',
            'image' : {
                'smallImageUrl': SMALL_IMAGE_URL,
                'largeImageUrl': LARGE_IMAGE_URL
            }
        },
        'reprompt': {            
        },
        'directives': [
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

def get_delegate_response():
    print('Sending Delegate response')
    return {
        'version': '1.0',
        'response': {
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ]
        }
    }

def get_welcome_response():
    """ Prompt the user for the prayer
    """    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "What would you like me to pray with you? I can pray the Rosary and the Divine Mercy Chaplet."
    reprompt_text = "What would you like me to pray with you?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, speech_output,
        should_end_session, []))

def get_rosary_response():
    """ Prompt the user for the day of the week, since we can't get it
    """    
    session_attributes = {}
    card_title = "Rosary"
    speech_output = "What day of the week is it?"
    reprompt_text = "What day of the week is it?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, speech_output,
        should_end_session, []))


def build_empty_response():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
        "shouldEndSession": True
        }
    }



# --------------- Events ------------------


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response()


def on_can_fulfill_intent(can_fulfill_request): 
    print ("on_can_fulfill_intent reqiestId=" +can_fulfill_request['requestId'] +
           ". sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("intent: " + intent_name)
    
def on_intent(intent_request, session, context):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("intent: " + intent_name)

    dialogState = intent_request.get('dialogState', 'UNDEFINED');
    print('Dialog state is ' + dialogState)
    
        
    # Dispatch to your skill's intent handlers
    if intent_name == 'Cancel' or intent_name == 'AMAZON.CancelIntent':
        return get_farewell_response()
    elif intent_name == 'Rosary':
        return get_rosary_response()
    elif intent_name == 'DivineMercy':
        return build_divine_mercy_response()
    elif intent_name == 'AMAZON.HelpIntent' or intent_name == 'Help':
        return get_help_response()
    elif intent_name == "ForDay":
        if dialogState != 'COMPLETED' and dialogState != 'UNDEFINED':
            return get_delegate_response()
        else:
            day = intent.get('slots',DEFAULT_DAY_SLOTS) \
                        .get('day', DEFAULT_VALUES) \
                        .get('value', DEFAULT_VALUE).lower()
            if not day in DAYS_OF_WEEK:
                return bad_day_of_week_input(day, dialogState)
            return build_pray_response(MYSTERIES_MAP[day])
    elif intent_name == "ForMysteries":
        if dialogState != 'COMPLETED' and dialogState != 'UNDEFINED':
            return get_delegate_response()
        else:
            mysteries = intent.get('slots',DEFAULT_MYSTERIES_SLOTS) \
                              .get('mysteries', DEFAULT_VALUES) \
                              .get('value',DEFAULT_VALUE).lower().encode('utf8')
            if not mysteries in MYSTERIES:
                return bad_mysteries_input(mysteries, dialogState)
            return build_pray_response(mysteries)
    elif intent_name == "AMAZON.ResumeIntent":
        token=context['AudioPlayer']['token']
        return play_current(token, context['AudioPlayer']['offsetInMilliseconds'])
    elif intent_name == "AMAZON.PauseIntent":
        return playback_stop()
    elif intent_name == "AMAZON.NextIntent":
        token=context['AudioPlayer']['token']
        return play_next(token, 'REPLACE_ALL', None)
    elif intent_name == 'AMAZON.PreviousIntent':
        token=context['AudioPlayer']['token']
        return play_current(token, 0)
    elif intent_name == 'AMAZON.StartOverIntent':
        token=context['AudioPlayer']['token']
        return start_over(token)        
    elif (intent_name == 'AMAZON.LoopOffIntent' or
          intent_name == 'AMAZON.LoopOnIntent' or
          intent_name == 'AMAZON.RepeatIntent' or
          intent_name == 'AMAZON.ShuffleOffIntent' or
          intent_name == 'AMAZON.ShuffleOnIntent'):
        return not_supported()
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
    return build_empty_response()


def on_playback_finished(finished_request):
    return build_empty_response()


def on_playback_stopped(stopped_request):
    print("Playback stopped for " + stopped_request['token'])
    return build_empty_response()



def on_playback_nearly_finished(nearly_finished_request):
    print("playing next prayer")
    token = nearly_finished_request['token']
    return play_next(token, 'ENQUEUE', token)

def play_next(token, playBehavior, expectedPrevious):
    current_data = TokenData.from_token(token)
    next_data = current_data.get_next()
    if next_data:
        print ("Playing " + next_data.do_print())
        return {
           'version': '1.0',
           'response': {
               'directives': [
                   {
                       'type': 'AudioPlayer.Play',
                       'playBehavior': playBehavior,
                       'audioItem': {
                           'stream': {
                               'token': next_data.get_token(),
                               'url': next_data.get_audio(),
                               'offsetInMilliseconds': 0,
                               'expectedPreviousToken': expectedPrevious
                           }
                       }
                   }
               ]
           }
       }
    else:
        print ("Finishing")
        return build_empty_response()

def on_next_command(play_request, context):
    print("Advancing")
    apContext = context['AudioPlayer']
    for x in apContext:
        print (x)
        print (apContext[x])
        
    for y in context:
        print (y)
   
        
    token = context['AudioPlayer']['token']
    return play_next(token, 'REPLACE_ALL', None)

def on_previous_command(play_request, context):
    print("Going back")
    token=context['AudioPlayer']['token']
    return play_current(token, 0)

def on_play_command(play_request, context):
    print("Resuming prayer")
    token = context['AudioPlayer']['token']
    return play_current(token, context['AudioPlayer']['offsetInMilliseconds'])

def play_current(token, offset):
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
                            'offsetInMilliseconds': offset
                        }
                    }
                }
            ]
        }
    }
   

def on_playback_failed(request):
    print ("Playback failed: " + request['error']['type']
           + ":" + request['error']['message'])
    return playback_stop()

def playback_stop():
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

    if (event.has_key('session') and event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.43e06ff9-fe37-4785-ad97-76508f4a2896"):
         raise ValueError("Invalid Application ID")


    print("Processing event: " + event['request']['requestId']
          + ": " + event['request']['type'])

    default_context = { 'AudioPlayer':
                {
                    'token': RosaryTokenData('Joyful','SignOfTheCross',0,0).get_token(),
                    'offsetInMilliseconds':0
                }
    }

    context = event.get('context',default_context)
        
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], context)
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
    elif event['request']['type'] == "AudioPlayer.PlaybackFailed":
        return on_playback_failed(event['request'])
    elif event['request']['type'] == "PlaybackController.PlayCommandIssued":
        return on_play_command(event['request'], context)
    elif event['request']['type'] == "PlaybackController.NextCommandIssued":
        return on_next_command(event['request'], context)
    elif event['request']['type'] == "PlaybackController.PreviousCommandIssued":
        return on_previous_command(event['request'], context)
    elif event['request']['type'] == "System.ExceptionEncountered":
        handle_exception(event['request'])
    elif event['request']['type'] == "CanFulfillIntentRequest":
        return on_can_fulfill_intent(event['request'])

