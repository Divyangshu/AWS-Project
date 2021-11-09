from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import boto3

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/sound", methods = ["GET", "POST"])
@cross_origin()
def sound():
	if request.method == "POST":
		text = request.form['texttranslate']
		sourcelanguage = request.form['slanguage']
		targetlanguage = request.form['tlanguage']
		
		translate = boto3.client(service_name='translate',region_name='us-east-1') 
		result = translate.translate_text(Text=text, SourceLanguageCode=sourcelanguage,TargetLanguageCode=targetlanguage) 
		
		translated = open("static/translated.txt","w+")
		translated.write(str(result["TranslatedText"]))
		
		polly = boto3.client(service_name='polly',region_name='us-east-1')

		print('Starting the Polly Service')

		response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',
					 Text=result["TranslatedText"])

		file = open('static/speech.mp3', 'wb')
		file.write(response['AudioStream'].read())
		file.close()
		print("Polly's output stored !")
		return render_template("index.html",conversion="Your Text has been converted to your required language")
	else:
		return render_template("index.html")


@app.route("/sentiment", methods = ["GET", "POST"])
@cross_origin()
def sentiment():
	if request.method == "POST":
		text = request.form['texttranslate']
		targetlanguage = request.form['tlanguage']
		comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
		result = comprehend.detect_sentiment(Text=text, LanguageCode=targetlanguage)
		
		return render_template("index.html",result=result['Sentiment'])
	else:
		return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)