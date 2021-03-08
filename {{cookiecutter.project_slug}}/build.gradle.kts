plugins {
    base
    id("org.schnabelsoft.gradle.python") version "0.2.0"
    id("com.palantir.docker") version "0.26.0"
    id("com.google.cloud.tools.minikube") version "1.0.0-alpha.3"
}

import org.schnabelsoft.gradle.python.plugin.*

docker {
    name = "schnabel/app"
    tag("foo", "0.1.0")
    files(file("Pipfile"), file("Pipfile.lock"), file("src/"))
}

tasks.register("createTestNamespace") {
    group = "minikube"
    doLast() {
        exec() {
            commandLine(listOf("kubectl", "create", "namespace", "foo-integration-test"))
        }
    }
}

tasks.register("deleteTestNamespace") {
    group = "minikube"
    doLast() {
        exec() {
            commandLine(listOf("kubectl", "delete", "namespace", "foo-integration-test"))
        }
    }
}

tasks.register("deployFoo") {
    group = "test"
    dependsOn("createTestNamespace")
    doFirst {
        exec() {
            environment(minikube.getDockerEnv("minikube"))
            commandLine(listOf("kubectl", "apply", "-n", "foo-integration-test", "-f", "src/test/foo-deployment.yaml"))
        }        
        exec() {
            commandLine(listOf("bash", "-c", "wget -qO- --retry-connrefused -t 100 --waitretry 1 http://$(minikube ip):30000/openapi.json &> /dev/null"))
        }        
    }
}

tasks.register<PipenvRunTask>("integrationTest") {
    group = "test"
    dependsOn("deployFoo", "build")
    command = "pytest src/test/integration"
    finalizedBy("deleteTestNamespace")
}

tasks.register<PipenvRunTask>("loadTest") {
    group = "test"
    dependsOn("deployFoo", "build")
    command = "locust -f src/test/load/locustfile.py --headless -u 100 -r 10 --host http://192.168.49.2:30000 --run-time 5min"
    finalizedBy("deleteTestNamespace")
}

tasks.register<PipenvRunTask>("load_spacy_model") {
    group = "python"
    dependsOn("pipenv")
    command = "python -m spacy download en_core_web_md"
    outputs.dir(file("$buildDir/venv"))
}

tasks.named("pytest") {
    dependsOn("load_spacy_model")
}

tasks.named("build") {
    dependsOn("docker")
}

tasks.named<Exec>("docker") {
    dependsOn("pytest")
    doFirst() {
        var dockerEnv = minikube.getDockerEnv("minikube")
        environment(dockerEnv)
    }
}
