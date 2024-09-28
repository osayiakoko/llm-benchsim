.PHONY: helm-install helm-upgrade helm-uninstall

helm-install:
	@helm install llm-benchsim ./llm-benchsim-chart

helm-upgrade:
	@helm upgrade llm-benchsim ./llm-benchsim-chart

helm-uninstall:
	@helm uninstall llm-benchsim
