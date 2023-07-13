var wwwRoot = window.location.href.split("/")[0];

var weTubeYellowPages = {
    "Name-1" :		["9XXXXXXXXXX", "webRTC-ext", "webRTC-ext"],
    "Name-2" :		["9XXXXXXXXXX", "webRTC-ext", "webRTC-ext"],
    "Name-3" :		["9XXXXXXXXXX", "webRTC-ext", "webRTC-ext"],
    "Name-3" :		["9XXXXXXXXXX", "webRTC-ext", "webRTC-ext"],
    "..." :		["9XXXXXXXXXX", "webRTC-ext", "webRTC-ext"]
}

var initDB = window.localStorage;
initDB.setItem("wssServer", "");
initDB.setItem("WebSocketPort", "8089");
initDB.setItem("ServerPath", "/ws");
initDB.setItem("profileName", weTubeUser);
initDB.setItem("SipDomain","");
initDB.setItem("SipUsername", weTubeYellowPages[weTubeUser][1]);
initDB.setItem("SipPassword", "");

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
    var id = uID();

    var id, key, val, pstn, sip, webRTC, buddyObj;

    for(key in weTubeYellowPages) {
        id = uID();
        val = weTubeYellowPages[key]; pstn = val[0]; webRTC = val[1]; sip = val[2];
        savePic((key == weTubeUser) ? "profilePicture" : "img-" + id + "-extension", wwwRoot + "/avatars/" + key + ".webp");
        if (key == weTubeUser) continue;

        json.DataCollection.push({
            Type: "extension",
            LastActivity: dateNow,
            ExtensionNumber: sip ? sip : pstn,
            MobileNumber: pstn,
            ContactNumber1: "",
            ContactNumber2: "",
            uID: id,
            cID: null,
            gID: null,
            jid: null,
            DisplayName: key,
            Description: "",
            Email: "",
            MemberCount: 0,
            EnableDuringDnd: false,
            Subscribe: false,
            SubscribeUser: "",
            AutoDelete: false
        });
        buddyObj = new Buddy("extension", id, key, webRTC, pstn, "", "", dateNow, "", "", null, false, false, null, false);
        AddBuddy(buddyObj, false, false, false, true);
    }
    json.TotalRows = json.DataCollection.length;
    localDB.setItem(me + "-Buddies", JSON.stringify(json));
}
