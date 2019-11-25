from app import app

import layout
app.layout = layout.make_layout
    
import callbacks

if __name__ == "__main__":
   app.run_server(debug=True)
