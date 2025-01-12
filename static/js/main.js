let pubnub;
let appChannel1 = "Temp-channel";

function hideTemp() {
    document.getElementById("initial_temperature").style.display = "none"
}

const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'pub-c-a4eb9e1f-e4e5-4791-8581-66149beb12a4',
        subscribeKey: 'sub-c-1b5226aa-e52c-474e-84e8-22b3645d0d83',
        userId: "CheckYourOxygen_User",
    });
    //create a channel
    const channel = pubnub.channel(appChannel1);
    //create a subscription
    const subscription = channel.subscription();

    pubnub.addListener({
        status: (s) => {
            console.log('Status', s.category);
        },
    });

    subscription.onMessage = (messageEvent) => {
        handleMessage(messageEvent.message);
    };

    subscription.subscribe();
};

const publishMessage = async (message) => {
    const publishPayload = {
        channel: appChannel1,
        message: message,
    };
    await pubnub.publish(publishPayload);
};

function handleMessage(message) {
    console.log('Message: ' + message);
    if (parseInt(message)) {
        console.log("MESSAGE FROM PUBNUB: ", message)
        document.getElementById("initial_temperature").value = message
    }
    else if (message == "Cup detected") {

    }
    else if (message == "No cup detected") {
    }

};