import requests
import json

appkey = "1724630275368"
appsecret = "549a26b527f429912abf81f18570030e"

def ConsultarNF(numeroNF):
    endpoint = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    payload ={
        "call": "ConsultarNF",
        "app_key": appkey,
        "app_secret": appsecret,
        "param": [
            {
                "tpNF":1,
                "nNF":numeroNF
            }
        ]
    }

    try:
        response = requests.post(endpoint,json=payload)
        resultado = response.json()
        #print("===== RETORNO DA API =====")
        #print(json.dumps(resultado, indent=2, ensure_ascii=False))
        #print("===========================")

        idPedido = resultado.get("compl", {}).get("nIdPedido")
        print (f"Código do Pedido: {idPedido}")

        if not idPedido:
            raise ValueError(f"Nota {numeroNF} não retornou o ID do pedido!")
        
        TrocarEtapa(idPedido)
        return True

    except Exception as e:
        return f"Erro: {e}"  # devolve erro
    
def TrocarEtapa(idPedido):
    endpointEtapa = "https://app.omie.com.br/api/v1/produtos/pedido/"
    payload={
        "call":"TrocarEtapaPedido",
        "app_key": appkey,
        "app_secret": appsecret,
        "param":[
            {
                "codigo_pedido": idPedido,
                "etapa":"70"
            }
        ]
    }

    try:
        responseEtapa = requests.post(endpointEtapa,json=payload)
        resultadoEtapa = responseEtapa.json()
        print("===== RETORNO DA API =====")
        print(json.dumps(resultadoEtapa, indent=2, ensure_ascii=False))
        print("===========================")

    except Exception as e:
        print("Erro na consulta:")
        print(e)

if __name__ == "__main__":
    ConsultarNF(32195)