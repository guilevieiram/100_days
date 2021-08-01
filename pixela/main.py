from src.tasks import Tasks, Pixela


def main() -> None:
	pixela: Tasks = Pixela()
	# pixela.create_user()
	pixela.create_graph(
		name="coding",
		unit="hours",
		data_type="int"
		)

if __name__ == "__main__":
	main()