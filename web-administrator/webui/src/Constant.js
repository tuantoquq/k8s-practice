const miner = "/miner";
const user = "/user";
const audit = "/audit";

const Root = {
    Default: {
        RootPage: "",
    },
    User: {
        Register: user + "/register",
        Login: user + "/login",
        Me: user + "/me",
        Lock: user + "/lock/",
        Unlock: user + "/unlock/",
        GetUser: user + "/",
    },
    Miner: {
        GetAll: miner + "/getall",
        GetOwnMiner: miner + "/getownminer",
        Create: miner + "/create",
        Update: miner + "/update",
        Delete: miner + "/delete",
        CreateDefault: miner + "/createdefault",
        UpdateDefault: miner + "/updatedefault",
        DeleteDefault: miner + "/deletedefault"
    },
    Audit: {
        GetAll: audit + "/getall",
    },
};

export default Root;
