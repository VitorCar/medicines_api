import os
import json
from rest_framework.response import Response
from rest_framework import views, status
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class SearchPharmacyAPIView(views.APIView):

    def post(self, request):

        city = request.data.get('city')
        state = request.data.get('state')

        if not city or not state:
            return Response(
                {"erro": "Por favor, forneça cidade e estado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        prompt = (
            f"Crie uma lista de 5 farmácias reais em {city}, {state}. "
            f"Retorne um array JSON puro. "
            f"Cada objeto deve ter estritamente as chaves: 'nome', 'endereco', 'cep'."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            clean_data = json.loads(response.text)

            return Response({
                "message": "Busca realizada com sucesso!",
                "city": city,
                "state": state,
                "suggestions_ia": clean_data
            }, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response(
                {"erro": "A IA retornou um formato inválido. Tente novamente."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        except Exception as e:
            return Response(
                {"erro": f"Falha ao consultar IA: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MedicineLeafletAPIView(views.APIView):

    def post(self, request):

        remedy = request.data.get('remedy')

        if not remedy:
            return Response({
                "erro": "Por favor, forneça o remédio. "
            }, status=status.HTTP_400_BAD_REQUEST
            )

        prompt = (
            f"Crie uma ficha técnica JSON para o medicamento '{remedy}'. "
            f"Preencha os campos abaixo respeitando rigorosamente o limite de caracteres: \n"
            f"- nome: Nome oficial.\n"
            f"- composicao_resumida: Principais ativos (máx 80 chars).\n"
            f"- indicacao_principal: Para que serve (máx 80 chars).\n"
            f"- posologia_adulto: Resumo de dose adulta (máx 80 chars).\n"
            f"- contraindicacao_chave: Principal risco (máx 100 chars)."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            clean_data = json.loads(response.text)

            return Response({
                "message": "Busca realizada com sucesso!",
                "remedy": remedy,
                "suggestions_ia": clean_data
            }, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response(
                {"erro": "A IA retornou um formato inválido. Tente novamente."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        except Exception as e:
            return Response(
                {"erro": f"Falha ao consultar IA: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
