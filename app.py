# import sys
# import os
# from flask import Flask, render_template, request, jsonify

# # Add the project root directory to Python path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(project_root)

# # Import Smobilpay services
# from smobilpay.services.quote_service import QuoteService
# # from smobilpay.services.cashin_service import CashinService
# from smobilpay.services.collection_service import CollectionService
# from smobilpay.services.payment_status_service import PaymentStatusService
# from smobilpay.services.cashout_service import CashoutService

# app = Flask(__name__)

# # Payment route
# @app.route('/')
# def checkout():
#     return render_template('index.html')

# @app.route('/process_payment', methods=['POST'])
# def process_payment():
#     data = request.json  # Receive JSON data from frontend
#     payment_option = data.get("paymentOption")
#     amount = data.get("amount")  # Dynamic amount from frontend
#     service_number = data.get("serviceNumber")  # Dynamic service number (user's phone)

#     try:
#         # Step 1: Fetch Cashouts (if needed)
#         cashout_service = CashoutService()
#         cashouts = cashout_service.fetch_cashouts(service_id=20053)
#         pay_item_id = cashouts[0].payItemId

#         # Step 2: Request a Quote
#         quote_service = QuoteService()
#         quote = quote_service.request_quote(pay_item_id, amount=int(amount))  # Use dynamic amount
#         quote_id = quote.quoteId

#         # Step 3: Execute Collection
#         collection_service = CollectionService()
#         collect_data = {
#             "quoteId": quote_id,
#             "customerPhonenumber": data.get("237653384869"),  # Using user's phone as serviceNumber
#             "customerEmailaddress": data.get("bleo71639@gmail.com"),
#             "customerName": data.get("Blanco"),
#             "customerAddress": data.get("Makepe"),
#             "serviceNumber": service_number,  # Dynamically filled
#             "trid": data.get("123456796655472234")
#         }
#         collect = collection_service.execute_collection(collect_data)

#         # Step 4: Check Payment Status
#         payment_status_service = PaymentStatusService()
#         payment_status = payment_status_service.fetch_payment_status(ptn=collect.ptn)

#         # Return status to frontend
#         return jsonify({
#             "status": payment_status.get("status"),
#             "message": "Payment processed successfully",
#             "transactionId": collect.trid
#         })

#     except Exception as e:
#         # Handle errors and return failure message
#         return jsonify({"status": "error", "message": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)



import sys
import os
from flask import Flask, render_template, request, jsonify

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import Smobilpay services
from smobilpay.services.quote_service import QuoteService
from smobilpay.services.collection_service import CollectionService
from smobilpay.services.payment_status_service import PaymentStatusService
from smobilpay.services.cashout_service import CashoutService

app = Flask(__name__)

# Payment route
@app.route('/')
def checkout():
    return render_template('index.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json  # Receive JSON data from frontend
    payment_option = data.get("paymentOption")
    amount = data.get("amount")
    service_number = data.get("serviceNumber")

    # Validate input data
    if not all([payment_option, amount, service_number]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        # Step 1: Fetch Cashouts (if needed)
        cashout_service = CashoutService()
        cashouts = cashout_service.fetch_cashouts(service_id=20053)
        pay_item_id = cashouts[0].payItemId

        # Step 2: Request a Quote
        quote_service = QuoteService()
        quote = quote_service.request_quote(pay_item_id, amount=int(amount))
        quote_id = quote.quoteId
        print(quote_id)

        # Step 3: Execute Collection
        collection_service = CollectionService()
        collect_data = {
            "quoteId": quote_id,
            "customerPhonenumber": "237654511241",
            "customerEmailaddress": "bleo71639@gmail.com",
            "customerName": "blanco",
            "customerAddress": "makepe",
            "serviceNumber": service_number,
            "trid": "1234567966554722355"
        }
        collect = collection_service.execute_collection(collect_data)

        # Use hardcoded PTN instead of relying on collection response
        ptn = collect.ptn  # Replace with your actual hardcoded PTN

        # Step 4: Check Payment Status
        payment_status_service = PaymentStatusService()
        payment_status = payment_status_service.fetch_payment_status(ptn=ptn)
        print(payment_status)

        # Return status to frontend
        return jsonify({
            "status": payment_status[0].status,
            "message": "Payment processed successfully",
            "transactionId": collect_data["trid"]  # Use the hardcoded TRID
        })

    except Exception as e:
        # Log the full exception for debugging
        app.logger.error(f"An error occurred: {str(e)}", exc_info=True)
        # Handle errors and return failure message
        return jsonify({"status": "error", "message": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
