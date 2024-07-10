from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from summary.models import User_data

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

def _login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=authenticate(request,username=email,password=password)
        # print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Login Failed")
       
        # return render(request,'login.html',context=context)
    return HttpResponse("Login Page")

@login_required
def Home_page(request):
    return render(request,'home.html')


@login_required
def _logout(request):
    logout(request)
    return redirect("/")

import json

@login_required
def get_transcription(request):
    if request.method=='POST':
        # url=request.body
        # str_object = url.decode("UTF-8")
        # url_dict = json.loads(str_object) 
        # video_url = url_dict.get('videoUrl', '')
        video_url=request.POST.get('video_url')
        res = User_data.objects.filter(youtube_link=video_url)        
        if not res.exists():
            from pytube import YouTube
            import whisper

            youtube=YouTube(url=video_url

            )
            video_stream=youtube.streams.get_highest_resolution()
            video_stream.download()

# Get th    e video filename
            video_filename = video_stream.default_filename

            # Transcribe the video using Whisper

            model = whisper.load_model("base.en")
            transcription = model.transcribe(video_filename)
            result=transcription.get("text")

            import openai

            openai.api_key = "Your api key here"
            prompt = f"summarize this '{result}'"

            messages = [
                {"role": "user", "content": prompt},
            ]

            response = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=[{"role":"user", "content":prompt}], max_tokens=1024, temperature=0.5
    )
    # Extract the generated summary from the API response
            summary = response.choices[0].message.content
            print(summary)

            # with open('text.txt','w') as f:
            #     f.write(result)
            #     # f.close()
            #     f.write("===========summ")
            #     # f.write(summary)
            #     f.close()

            user=User_data.objects.create(youtube_link=video_url,summary=result,ai_summary=summary,user=request.user)
            return render(request,'result.html',context={'summary':result,'ai_summary':summary})

        else:
            for res in res:
                result=res.summary
                summary=res.ai_summary
                break

            existing_data=User_data.objects.filter(youtube_link=video_url,user=request.user)
            if not existing_data.exists():
                user=User_data.objects.create(youtube_link=video_url,summary=result,user=request.user,ai_summary=summary)
            else:
                import datetime
                for data in existing_data:
                    data.updated_at=datetime.datetime.now()
                    data.save()
            
            
            
    # Extract the generated summary from the API response
    #         import openai

    #         openai.api_key = ""
    #         prompt = f"summarize this '{result}'"

    #         messages = [
    #             {"role": "user", "content": prompt},
    #         ]

    #         response = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=[{"role":"user", "content":prompt}], max_tokens=1024, temperature=0.5
    # )
    # # Extract the generated summary from the API response
    #         summary = response.choices[0].message.content
    #         print(summary)
            return render(request,'result.html',context={'summary':result,
                                                         'ai_summary':summary})


def about(request):
    return render(request,'about.html')
from django.contrib.auth.models import User
def register(request):
    if request.method=='POST':
        try:
            email=request.POST.get('email')
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            username=request.POST.get('username')
            password=request.POST.get('password')
            User.objects.create_user(email=email,first_name=fname,last_name=lname,username=username,password=password)
            return redirect('/')
        except Exception as e:
            return HttpResponse("error"+ str(e))
        



@login_required
def history(request):
    user_data=User_data.objects.filter(user=request.user)
    return render(request,'history.html',context={'user_data':user_data})
