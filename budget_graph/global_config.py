import tomllib


class GlobalConfig:
	global_cache_enable: bool = None
	redis_enable: bool = None
	timeit_enable: bool = None
	recaptcha_enable: bool = None
	localization_enable: bool = None

	@staticmethod
	def set_config():
		from sys import path as sys_path
		sys_path.append('../')
		with open('conf.toml', 'rb') as f:
			conf_data = tomllib.load(f)

			# vars are written only once when the application is launched and are then immutable

			# cache
			GlobalConfig.global_cache_enable = (
					GlobalConfig.global_cache_enable or conf_data.get('cache').get('global_cache_enable')
			)
			GlobalConfig.redis_enable = (
				(GlobalConfig.redis_enable or conf_data.get('cache').get('redis_enable'))
				# if caching is disabled, then Redis is not connected in any case
				if GlobalConfig.global_cache_enable else False
			)

			# timeit
			GlobalConfig.timeit_enable = (
					GlobalConfig.timeit_enable or conf_data.get('timeit').get('timeit_enable')
			)

			# recaptcha
			GlobalConfig.recaptcha_enable = (
					GlobalConfig.recaptcha_enable or conf_data.get('recaptcha').get('recaptcha_enable')
			)

			# localization
			GlobalConfig.localization_enable = (
					GlobalConfig.localization_enable or conf_data.get('localization').get('localization_enable')
			)
