"""Mock dictionaries only: never read real environment variables or credentials."""
import json

def startup(config,server_only):
    invalid=[]
    version=config.get('DATA_VERSION')
    maximum=config.get('MAX_WORDS')
    secret=server_only.get('SIGNING_SECRET')
    if type(version) is not str or not version.strip():invalid.append('DATA_VERSION')
    if type(maximum) is not int or maximum<=0:invalid.append('MAX_WORDS')
    if type(secret) is not str or not secret.strip():invalid.append('SIGNING_SECRET')
    if invalid:
        return None,{'status':'startup_blocked','missing_or_invalid':invalid}
    internal={'data_version':version,'maximum_words':maximum,'signing_secret':secret}
    # Construct a new allowlisted public record, never serialize internal state.
    public={'status':'ready','data_version':version,'maximum_words':maximum}
    return internal,public

config={'DATA_VERSION':'classroom-v1','MAX_WORDS':80}
mock_private={'SIGNING_SECRET':'fictional-placeholder-not-a-real-credential',
              'UNRELATED_SECRET':'unrelated-fictional-sentinel'}
internal,public=startup(config,mock_private)
_,missing=startup({'MAX_WORDS':80},mock_private)
_,absent_secret=startup(config,{})
_,changed=startup({'DATA_VERSION':'classroom-v1','MAX_WORDS':60},mock_private)
assert public=={'status':'ready','data_version':'classroom-v1','maximum_words':80}
assert missing=={'status':'startup_blocked','missing_or_invalid':['DATA_VERSION']}
assert absent_secret=={'status':'startup_blocked','missing_or_invalid':['SIGNING_SECRET']}
assert changed['maximum_words']==60 and internal['signing_secret']==mock_private['SIGNING_SECRET']
serialized=json.dumps([public,missing,absent_secret,changed])
assert all(value not in serialized for value in mock_private.values())
assert set(public)=={'status','data_version','maximum_words'}
print('Public startup record:',public)
print('Missing version:',missing)
print('Absent server-only placeholder:',absent_secret)
print('Changed public length setting:',changed)
print('Mock private values absent from every emitted record:',True)
print('No credential store, signing, rotation, deployment or real environment access is implemented.')
