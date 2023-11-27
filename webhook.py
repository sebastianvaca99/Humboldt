#Importar librerias y funciones necEsarias para el funcionamiento del webhook
import logging
from db import  run_query,verificar_usuario, get_proyectos, verificar_permiso_proyecto, set_proyecto

#Variables globales qque guardan los resultados de las comnsultas
query_results = None
textual_query_results = None
saved_password = None
user_id = None

def get_query_results():
    global query_results
    return query_results

def get_textual_query_results():
    global textual_query_results
    return textual_query_results

#Funcion que procesa la peticion del usuario cuando es enviada a dialogflow
def processRequest(req):

    #Obtiene el resultado de la peticion
    result = req.get("queryResult")
    logging.debug(f"Result:{result}")

    #Obtiene el intent de la peticion
    intent = result.get("intent").get('displayName')
    logging.debug(f"Intent:{intent}")

    #Obtiene el query del usuario
    user_query = result.get("queryText")
    logging.debug(f"User's query: {user_query}")

    #Se verifica el valor del intent para saber que respuesta dar o como procesar la peticion
    if intent == 'SALUDO_VERIFICACION':
        parameters = result.get("parameters")
        logging.debug(f"Parameters: {parameters}")
        email = parameters.get("email")
        logging.debug(f"Email: {email}")

        id, password = verificar_usuario(email)
        logging.debug(f"ID: {id}, Password: {password}")

        if password is not None:
            fulfillmentText="Tienes habilitado el acceso a el espacio interactivo, ahora ingresa tu contraseña:"
            global saved_password
            global user_id
            user_id = id
            saved_password = password
        else:
            fulfillmentText="No tienes acceso a el uso de el espacio interactivo"

    elif intent == 'SALUDO_VERIFICACION_CONTRASENIA':
        parameters = result.get("parameters")
        logging.debug(f"Parameters: {parameters}")
        contrasenia = parameters.get("any")
        logging.debug(f"Contrasenia: {contrasenia}")

        if contrasenia == saved_password:
            fulfillmentText="La contraseña es correcta. \n\n Deseas una lista de los proyectos?"
        else:
            fulfillmentText="La contraseña es incorrecta. No tienes acceso al espacio interactivo."

    elif intent == 'PROYECTOS':
        
        proyectos = get_proyectos()
        logging.debug(f"Proyectos: {proyectos}")
        
        proyectos_str = "\n".join(f"{i+1}. {proyecto}" for i, proyecto in enumerate(proyectos))

      
        fulfillmentText = f"Los proyectos son:\n\n{proyectos_str}\n\n¿Cuál deseas consultar?"

    elif intent == 'PROYECTOS_SELECCION':
        parameters = result.get("parameters")
        logging.debug(f"Parameters: {parameters}")
        number = int(parameters.get("number"))
        logging.debug(f"Number: {number}")
        permisos = verificar_permiso_proyecto(user_id, number)

        if permisos is not None:
            set_proyecto(number)
            fulfillmentText = f"Posees los permisos de acceso a la informacion de este proyecto.\n\nDeseas ver los metadatos del proyecto o consultar la informacion de consulta de este?"
        else:
            fulfillmentText = f"No tienes los permisos de acceso a la informacion de este proyecto"

    elif intent == 'CONSULTA_EXPORTACIONES_QUERY':
        global query_results
        parameters = result.get("parameters")
        logging.debug(f"Parameters: {parameters}")
        number = int(parameters.get("number1"))
        logging.debug(f"Number: {number}")

        query_results = run_query(number)

        fulfillmentText = "Perfecto Visualiza los resultados de tu consulta. \n\nDeseas realizar otra consulta?"
        
        return {
            "fulfillmentText": fulfillmentText
        }
    
    elif intent == 'CONSULTA_MERCADOS':
            
            fulfillmentText = "Que información te gustaría conocer: \n\n1. Perfil de negocios de Colombia.\n2. Beneficios exportadores colombianos.\n3. Tratados libre comercio.\n4. Perfil económico de Colombia.\n5. Producción en departamentos.\n6. Iniciativas y políticas gubernamentales recientes.\n7. Oportunidades emergentes.\n8. Análisis de riesgo"
            
            return {
                "fulfillmentText": fulfillmentText
            }

    elif intent == 'CONSULTA_MERCADOS_QUERY':
        global textual_query_results
        parameters = result.get("parameters")
        logging.debug(f"Parameters: {parameters}")
        number = int(parameters.get("number2"))
        logging.debug(f"Number: {number}")

        textual_query_results = number

        fulfillmentText = "La informacion ha sido cargada en la pantalla. Presiona el boton para visualizarla. \n\n Deseas conocer algo mas del mercado?"
        
        return {
            "fulfillmentText": fulfillmentText
        }
    

    elif intent == 'CONSULTA_EXPORTACIONES_QUERY_SI':
        return {
            "followupEventInput": {
                "name": "reiniciare",
                "languageCode": "es",
               
        }
    }

    elif intent == 'CONSULTA_EXPORTACIONES_QUERY_NO':
        return {
            "followupEventInput": {
                "name": "reiniciarp",
                "languageCode": "es",
                "parameters": {
                    "number": 1
                }
        }
    }

    elif intent == 'CONSULTA_MERCADOS_QUERY_SI':
        return {
            "followupEventInput": {
                "name": "inteligencia",
                "languageCode": "es",
                "parameters": {
                    "mercados": "mercados"
                }
        }
    }
    
    elif intent == 'CONSULTA_MERCADOS_QUERY_NO':
        return {
            "followupEventInput": {
                "name": "reiniciarp",
                "languageCode": "es",
                "parameters": {
                    "number": 1
                }
        }
    }

    elif intent == 'PROYECTOS_SELECCION_METADATOS_SI':
        return {
            "followupEventInput": {
                "name": "reiniciarp",
                "languageCode": "es",
                "parameters": {
                    "number": 1
                }
        }
    }

    else:
        fulfillmentText = "Lo siento no entiendo lo que quieres decir"

    return {
        "fulfillmentText": fulfillmentText
    }