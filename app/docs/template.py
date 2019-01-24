doc_temp={
    "openapi": "3.0.0",
    "info": {
      "title": "IReporter",
      "description": "API for ireporter application",
      "contact": {
        "email": "josean@andela.com",
        "url": "https://www.joelpatrick.com"
      },
      "termsOfService": "https://www.joelpatrick.com/terms",
      "version": "v1"
    },
    "paths":{
      "/ireporter/api/v2/auth/login":{
        "post": {
            "operationId": "login",
            "tags": [
              "login"
            ],
            "requestBody": {
              "required": True,
              "content": {
                "application/json": {
                  "schema": {
                    "properties": {
                      "username": {
                        "type": "string",
                        "example": "admin"
                      },
                      "password": {
                        "type": "string",
                        "example": "admin"
                      }
                    },
                    "required": [
                      "username",
                      "password"
                    ]
                  }
                }
              }
            },
            "responses": {
              "201": {
                "description": "Succesfully logged in"
              }
            }
      }
  }
    },
    "components": {
      "securitySchemes": {
        "bearerAuth": {
          "type": "http",
          "scheme": "bearer",
          "bearerFormat": "JWT"
        }
      }
    }
  }