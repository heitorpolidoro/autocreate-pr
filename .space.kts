/**
* JetBrains Space Automation
* This Kotlin-script file lets you automate build activities
* For more info, see https://www.jetbrains.com/help/space/automation.html
*/

job("Hello World!") {
    container(displayName = "Say Hello", image = "hello-world")
}


job("Example shell script") {
    container(displayName = "Say Hello", image = "ubuntu") {
        shellScript {
            content = """
                echo Hello
                echo World!
            """
        }
    }
}

job("batata") {
container("amazoncorretto:17-alpine") {
    kotlinScript { api ->
        api.space().projects.automation.deployments.start(
            project = api.projectIdentifier(),
            targetIdentifier = TargetIdentifier.Key("github-marketplace"),
            version = "1.0.0",
            // automatically update deployment status based on a status of a job
            syncWithAutomationJob = true
        )
    }
}
}