from rest_framework.views import APIView
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
import pytesseract
from PIL import Image
import uuid
import asyncio
import fitz  # PyMuPDF

import edge_tts
@method_decorator(csrf_exempt, name='dispatch')
class TextToSpeechView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    async def generate_audio(self, text, file_path):
        communicate = edge_tts.Communicate(text, "uz-UZ-SardorNeural")
        await communicate.save(file_path)

    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response({"error": "No text provided"}, status=400)

        try:
            file_path = f"{uuid.uuid4()}.mp3"

            asyncio.run(self.generate_audio(text, file_path))

            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
def home(request):
    return render(request, "index.html")

from rest_framework.permissions import AllowAny
import fitz

@method_decorator(csrf_exempt, name='dispatch')
class PDFToSpeechView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    async def generate_audio(self, text, file_path):
        communicate = edge_tts.Communicate(text, "uz-UZ-SardorNeural")
        await communicate.save(file_path)

    def post(self, request):
        try:
            file = request.FILES.get("file")

            if not file:
                return Response({"error": "No file uploaded"}, status=400)

            pdf_bytes = file.read()

            if not pdf_bytes:
                return Response({"error": "Empty file"}, status=400)

            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            text = ""
            for page in doc:
                text += page.get_text()

            if not text.strip():
                return Response({"error": "No readable text"}, status=400)

            file_path = f"{uuid.uuid4()}.mp3"

            asyncio.run(self.generate_audio(text, file_path))

            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')

        except Exception as e:
            return Response({"error": str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ImageToSpeechView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    async def generate_audio(self, text, file_path):
        communicate = edge_tts.Communicate(text, "uz-UZ-SardorNeural")
        await communicate.save(file_path)

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No image uploaded"}, status=400)

        try:
            image = Image.open(file)

            # OCR
            text = pytesseract.image_to_string(image)

            if not text.strip():
                return Response({"error": "No text found in image"}, status=400)

            file_path = f"{uuid.uuid4()}.mp3"

            asyncio.run(self.generate_audio(text, file_path))

            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')

        except Exception as e:
            return Response({"error": str(e)}, status=500)