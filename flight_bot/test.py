from src.view.ui import TerminalUserInteface
from src.model.user_model import User


if __name__ == "__main__":

	t = TerminalUserInteface()

	res = t.accquire_user(["phone", "name"])
	print(res)

	u = User(phone="1234546789", first_name="gui")
	print(u.__dict__)

