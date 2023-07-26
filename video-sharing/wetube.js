var wwwRoot = window.location.href.split("/")[0];

var weTubeYellowPages = {
    "Frannie" :		["",            "7160", "7160"],
    "Dad" :		["95184613259", "7150", "7150"],
    "Mom" :		["94109495047", "7140", "7140"],
    "UncleDaniel" :	["98605978618", "7130", "7130"],
    "KK" :		["94438388483", "7120", "7120"],
    "DiDi" :		["94432554925", "7110", "7110"],
    "G" :		["94437569795", "7100", "7100"]
}
var weTubeServer = "mckspot.net";

var initDB = window.localStorage;
var weTubeExt = weTubeYellowPages[weTubeUser][1];
initDB.setItem("wssServer", weTubeServer);
initDB.setItem("WebSocketPort", "8089");
initDB.setItem("ServerPath", "/ws");
initDB.setItem("profileName", weTubeUser);
initDB.setItem("SipDomain",weTubeServer);
initDB.setItem("SipUsername", weTubeExt);
initDB.setItem("SipPassword", "789889");
initDB.setItem("VoiceMailSubscribe", "0");

initDB.setItem("ChatEngine", "XMPP");
initDB.setItem("XmppServer", weTubeServer);
initDB.setItem("XmppWebsocketPort", "7443");
initDB.setItem("XmppWebsocketPath", "/ws");
initDB.setItem("XmppDomain", weTubeServer);
initDB.setItem("profileUser", weTubeExt);

async function blobToBase64 (blob) {
  var reader = new FileReader();
  reader.readAsDataURL(blob);
  return new Promise(resolve => {
    reader.onloadend = () => {
      resolve(reader.result);
    }
  });
}

async function savePic(dbkey, uri) {
    fetch(uri).then((rsp) => rsp.blob()).then((blob) => blobToBase64(blob)).then((base64) => initDB.setItem(dbkey, base64));
}

function InitGlobalBuddies () {
    var me = getDbItem("profileUserID", null);
    if (me == null) return;

    var json = JSON.parse(localDB.getItem(profileUserID + "-Buddies"));
    if(json == null) json = InitUserBuddies();

    var dateNow = utcDateNow();
    var buddyObj = null;

    var id, jid, key, val, pstn, sip, webRTC, buddyObj;

    for(key in weTubeYellowPages) {
        val = weTubeYellowPages[key]; pstn = val[0]; webRTC = val[1]; sip = val[2];
        if (key == weTubeUser) {
        	savePic("profilePicture", wwwRoot + "/avatars/" + key + ".webp");
		continue;
	}
	else {
	        id = uID(); jid =  sip + "@" + weTubeServer;
		savePic("img-" + id + "-extension", wwwRoot + "/avatars/" + key + ".webp");
	}

        json.DataCollection.push({
            Type: "xmpp",
            LastActivity: dateNow,
            ExtensionNumber: sip ? sip : pstn,
            MobileNumber: pstn,
            ContactNumber1: "",
            ContactNumber2: "",
            uID: id,
            cID: null,
            gID: null,
            jid: jid,
            DisplayName: key,
            Description: "",
            Email: "",
            MemberCount: 0,
            EnableDuringDnd: false,
            Subscribe: true,
            SubscribeUser: "",
            AutoDelete: false
        });
        buddyObj = new Buddy("xmpp", id, key, webRTC, pstn, "", "", dateNow, "", "", jid, false, false, null, false);
	AddBuddy(buddyObj, false, false, false, true);
    }
    json.TotalRows = json.DataCollection.length;
    localDB.setItem(me + "-Buddies", JSON.stringify(json));
}
