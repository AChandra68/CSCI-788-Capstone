import requests
import json
import random


# Define the endpoint URL -- served by the model running in Ollama
url = "http://localhost:11434/api/chat"


# Define the headers and payload
headers = {
   "Content-Type": "application/json"
}


# list of issues around which a therapy conversation spins
issues = [
           'OCD', 'dissociative fugue', 'personality disorders', 'parenting', 'alienation', 'avoidant personality disorder',
           'academic underachievement', 'substance abuse', 'ADHD', 'dissociative disorders', 'regret', 'mood disorders', 'infidelity',
           'isolation', 'antisocial personality disorder', 'self-doubt', 'eating disorders', 'discrimination', 'life transitions',
           'gender dysphoria', 'gender confusion', 'self-criticism', 'trauma', 'anxiety disorders', ' Borderline Personality Disorder',
           'social skills deficits', 'communication skills', 'financial stress', 'aging', 'self-sabotage', 'value clarification',
           'transphobia', 'spiritual issues', 'histrionic personality disorder', 'female orgasmic disorder', 'legal issues',
           'suicide attempts', 'addiction', 'guilt', 'time management', 'depression', 'emptiness', 'assertiveness', 'bereavement',
           'ableism', 'social isolation', 'negative self-talk', 'relationship problems', 'premature ejaculation', 'suicidal thoughts',
           'loneliness', 'excoriation disorder', 'time management issues', 'homophobia', 'impulse control issues', 'family conflict',
           'derealization disorder', 'gender identity', 'sexual pain disorder', 'psychotic disorders', ' separation anxiety', 'bullying',
           'dissociative identity disorder', 'career goals', ' indecisiveness', 'self-discovery', 'suicidal ideation', 'sorrow',
           "Tourette's syndrome", 'identity issues', 'spirituality', 'sexism', 'sexual dysfunction', 'panic attacks', 'indecisiveness',
           'body image issues', 'sexuality issues', 'learning disabilities', 'religious issues', 'stress management', 'autism spectrum disorder',
           'neurodevelopmental disorders', 'social anxiety', 'self-destructive behaviors', 'goal setting', 'schizoid personality disorder',
           'trichotillomania', 'low self-esteem', 'narcissistic personality disorder', 'self-harm', 'educational goals', 'work stress',
           'anger issues', 'career counseling', 'decision-making difficulties', 'risk assessment difficulties', "Asperger's Syndrome",
           "Tourette's Syndrome", 'shame', 'attention deficit hyperactivity disorder', 'family issues', 'female sexual arousal disorder',
           'schizotypal personality disorder', ' isolation', 'violence issues', 'loss', 'vaginismus', 'anger management issues', 'medical issues',
           'friendship issues', 'meaning of life issues', 'disconnection', 'dependent personality disorder', 'grief', 'hoarding disorder',
           'shyness', 'mindfulness', 'male orgasmic disorder', 'meaning of life', 'dyspareunia', 'sexual orientation issues',
           'heart break', 'retirement', 'sexuality', 'BDD', 'aggression issues', 'erectile dysfunction', 'depersonalization disorder',
           'life purpose', 'paranoid personality disorder', 'chronic pain', 'exam performance anxiety', 'purpose in life issues',
           'perfectionism', 'divorce', 'self-blame', 'anxiety', 'sadness', 'anger management', 'Autism Spectrum Disorder',
           'emotional regulation difficulties', 'stage performance anxiety', 'harassment', 'self-esteem issues', 'existential issues',
           'castration anxiety', 'sexual issues', 'xenophobia', 'amnesia', 'remorse', 'sleep disorders', 'procrastination', 'co-parenting',
           'dissociation', 'racism', 'glossophobia', 'job loss', 'loss of loved ones', 'loss of a pet'
       ]

# therapy sessions should conclude with notes based on this list
concludes_as = [
                   'motivate to see a professonal therapist', 'motivate to seek out help', 'suggest to discuss with a close friend',
                   'suggest to discuss with parents', 'promote self worth', 'promote discussion with the parties involved',
                   'as a helpful therapist and ask for another interaction after sometime to check on progress', 'you being the support system',
                   'promote self love', 'promote self growth', 'self acceptance', 'promote more socialization', 'seek professional help on socialization',
                   'being grateful in life for what we have', 'more positivity in life', 'being optimistic', 'getting a pet for emotional support'
               ]

# the session flow 
pace_and_approach = [
                       "deep and thoughtful", "slow and inquisitive", "supportive and hopeful", "calm and hopeful", "adviceful", 'steady and calm',
                       'responsible and sincere', 'client led based on therapist questions', 'therapist led and client responsive', 'solution based',
                       'finding root cause with deep analysis', 'mix of client emotional breakdown and venting to therapist', 'frustration filled client',
                       "progressive based on clien's feelings", 'fluid and smooth discussion', 'reflective and conscientious'
                   ]

# function to generate actual therapy conversation sessions
def generate_prompt():
   
   # randomly slect the issue type, approach and conclusion note of the session
   issue = random.choice(issues)
   approach = random.choice(pace_and_approach)
   conclusion = random.choice(concludes_as)
   payload = {
       "model": "llama3.1",
       "messages": [
           {
               "role": "user",
               "content": f"""You are a therapy conversation generator.
               Your need to generate a therapy conversation that is based on parameters you will be given. Do not stop writing until
               it is impossible to continue.
               Generate a therapy conversation with the following specifications:
               Issue: The main topic of the conversation should be {issue}.
               Pace and approach: The manner of expression in the conversation should be {approach}.
               Conclude as: The conversation should be concluded as "{conclusion}".
               Language: The choice of words and phrases in the conversation should be Everyday language.
               Therapist: The therapist, should be curious, loving, empathetic, and use simple language. The therapist should ask the right questions and make the client feel welcomed.
               Client: The client, should write messages of varying lengths and use simple language.
               Now generate the conversation, which should be as long as possible. Use the following output formatting, such that it's a dictionary:
               {{
                   "conversations": [
                       {{
                           "from": "client",
                           "value": "client's message."
                       }},
                       {{
                           "from": "therapist",
                           "value": "therapist's message"
                       }},
                       {{
                           "from": "client",
                           "value": "client's message"
                       }},
                       {{
                           "from": "therapist",
                           "value": "therapist's message"
                       }},
                       {{
                           // continue until the end of therapy conversating session in this way
                       }}
                   ]
               }}
               """
               # "content": f"""I'm building a synthetic dataset for therapy sessions. Give me as much exhaustive as possible list of two to four word long focused issue. For example, "heart break", "family issues", "work stress", "exam performance anxiety", "stage performance anxiety" are few example. Give me as exhaustive list as you can. The output should in a comma-separated list like: ["heart break", "family issues", ...]
               # """
           }
       ],
       "stream": False
   }
   return payload

# 
def generate_therapy_data(data_file, total_count = 10000):
  
   with open(data_file, 'a') as data_location:
       for iterator in range(total_count):
          
           print(f"Generating a conversation.....")
           # Send a POST request to the API
           response = requests.post(url, headers=headers, data=json.dumps(generate_prompt()))

           # Check if the request was successful
           if response.status_code == 200:
               response_json = response.json()
               content = response_json.get('message', {}).get('content', '')
               data_location.write(",\n")
               data_location.write(content)
           else:
               print(f"Request failed with status code {response.status_code}")


generate_therapy_data(data_file = "therapy_data.json", total_count=3)