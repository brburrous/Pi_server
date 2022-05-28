from app import app

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", use_reloader=False) #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.