@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    try:
        # Extract user ID for folder structure
        user_folder = f"user_{session['user_id']}"
        
        # Clean filename: replace spaces & special characters with underscores
        filename = re.sub(r"[^\w\-_.]", "_", file.filename)

        # Ensure extension is retained
        file_ext = os.path.splitext(filename)[-1]  # Get .pdf, .txt, etc.
        file_base_name = os.path.splitext(filename)[0]  # Get filename without extension
        public_id = f"{user_folder}/{file_base_name}"  

        # Detect resource type
        resource_type = "raw" if file_ext.lower() in [".pdf", ".txt", ".zip"] else "auto"

        # Upload to Cloudinary with forced attachment (preserves extension)
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type=resource_type,
            public_id=public_id,
            format=file_ext.replace(".", ""),  # Ensures correct extension
            attachment=True  # Forces correct download behavior
        )

        # Just use the secure_url directly from the upload result
        file_url = upload_result["secure_url"]

        # Save to database
        db = get_db()
        db.execute(
            '''INSERT INTO files (user_id, public_id, url, filename, resource_type, format) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (
                session['user_id'], 
                upload_result["public_id"], 
                file_url,  
                filename,
                upload_result["resource_type"],
                upload_result.get("format", file_ext.replace(".", ""))  
            )
        )
        db.commit()

        return jsonify({"message": "Upload successful", "file_url": file_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500