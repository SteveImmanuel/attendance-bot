from attbot import create_app, WEBHOOK_LISTEN, WEBHOOK_PORT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV

if __name__ == '__main__':
    app = create_app()
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)
