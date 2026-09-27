from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>E-Commerce Platform</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }

            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.12);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
                width: 90%;
                max-width: 650px;
            }

            .icon {
                font-size: 60px;
                margin-bottom: 15px;
            }

            h1 {
                font-size: 38px;
                margin-bottom: 12px;
            }

            p {
                font-size: 18px;
                opacity: 0.9;
                margin-bottom: 30px;
            }

            .status {
                display: inline-block;
                background: rgba(46, 204, 113, 0.2);
                border: 1px solid rgba(46, 204, 113, 0.5);
                padding: 10px 20px;
                border-radius: 30px;
                margin-bottom: 30px;
            }

            .status span {
                color: #2ecc71;
                font-weight: bold;
            }

            .buttons {
                display: flex;
                justify-content: center;
                gap: 15px;
                flex-wrap: wrap;
            }

            a {
                text-decoration: none;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.18);
                border: 1px solid rgba(255, 255, 255, 0.25);
                transition: 0.3s;
            }

            a:hover {
                background: white;
                color: #667eea;
                transform: translateY(-2px);
            }

            .tech {
                margin-top: 30px;
                font-size: 14px;
                opacity: 0.75;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="icon">🛒</div>

            <h1>E-Commerce Platform</h1>

            <p>
                Welcome to the backend API of our e-commerce application.
            </p>

            <div class="status">
                🟢 <span>Backend is running successfully</span>
            </div>

            <div class="buttons">
                <a href="/api/products/">
                    View Products API
                </a>

                <a href="/admin/">
                    Admin Panel
                </a>
            </div>

            <div class="tech">
                Django • Django REST Framework • MySQL
            </div>

        </div>

    </body>
    </html>
    """)