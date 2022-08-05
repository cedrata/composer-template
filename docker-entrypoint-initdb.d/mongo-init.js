const DB_ADMIN_USERNAME = 'admin'
const DB_ADMIN_PASSWORD = 'admin'

print('Start #################################################################');

// db = connect('mongodb://'+process.env.MONGO_INITDB_ROOT_USERNAME+':'+process.env.MONGO_INITDB_ROOT_PASSWORD+'@localhost:27017');
db = connect('mongodb://root:root@localhost:27017');

db = db.getSiblingDB('fastapi_auth_template')

db.createUser(
	{
		user: DB_ADMIN_USERNAME,
		pwd: DB_ADMIN_PASSWORD,
		roles: [{ role: 'dbOwner', db: 'fastapi_auth_template' }]
	}
)

db.createCollection('users')
db.users.insertMany(
	[
		{
			email: 'admin@email.com',
			username: 'admin',
			password: '$2b$12$N/LPnzvpHyE2KI2cuxhMz.3FSnF7MuoN6EeDKtE9yGiqMBVj3US/e',
			roles: ['admin'],
			"creation": new Date("2022-08-05T17:35:00.060Z"),
			"last_update": new Date("2022-08-05T17:35:00.060Z"),
		},
		{
			email: 'user@email.com',
			username: 'user',
			password: '$2b$12$bCT0LidMlwjjA1YCKtZkxeuc74CU1R1zxqE9ntSE7s7IYkP2fbtrK',
			roles: ['user'],
			"creation": new Date("2022-07-15T21:37:00.000Z"),
			"last_update": new Date("2022-07-15T21:37:00.000Z"),
		}
	]
)

print('END ###################################################################');
