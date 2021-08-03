from src.view.ui import TerminalUserInteface
from src.model.user_model import User


if __name__ == "__main__":

	t = TerminalUserInteface()

	res = t.accquire_user(["phone", "name"])
	print(res)

	u = User(phone="1234546789", first_name="gui")
	print(u.__dict__)

'''
export WEATHER_API_KEY=235ca50b277238427b332ff96edc15d1;
export TWILIO_SID=ACb62737daa2ca8914b38d013ac3946891;
export TWILIO_TOKEN=7641c51d4e8e4896502c1817daa71d24;
cd rain_bot;
python3 main.py;
cd ..;

export EMAIL_USER=guilhermevmanhaes@gmail.com;
export EMAIL_PASSWORD_PYTHON=wpknrxdfaupmbwyz;
export FLIGHT_API=oSVqZWhbO4RNWdpCT5kCbfA0abXwx6t-;
cd flight_bot;
python3 main.py;
cd ..;
'''