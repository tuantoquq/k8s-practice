import Background from "../../image/BackGround.jpg";
import React from "react";
import {
    TextField,
    Button,
    Paper,
    Grid,
    FormControlLabel,
    Checkbox,
    Box,
    Modal,
} from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Axios from "../../Api.js";
import Root from "../../Constant";

const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
};

export default function Login() {
    const navigate = useNavigate();
    const [checked, setChecked] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [notice, setNotice] = useState("");
    const [openRegister, setOpenRegister] = useState(false);
    const [noticeRegister, setNoticeRegister] = useState("");
    const [name, setName] = useState("");
    const [usernameRegister, setUsernameRegister] = useState("");
    const [passwordRegister, setPasswordRegister] = useState("");
    const [repeatPassword, setRepeatPassword] = useState("");
    const handleChange = (event) => {
        setChecked(event.target.checked);
    };
    const handleClickLogin = async (e) => {
        e.preventDefault();
        var data = {
            Username: username,
            Password: password,
            Role: checked ? 0 : 1,
        };
        try {
            await Axios.post(Root.User.Login, data).then((res) => {
                if (res.data == "No permission!") {
                    setNotice(
                        "Your account is locked, please contact to admin!"
                    );
                    return;
                }
                localStorage.setItem(
                    "token",
                    "Bearer " + res.data.access_token
                );
                setUsername("");
                setPassword("");
                if (checked) {
                    navigate("/audit");
                } else {
                    navigate("/data");
                }
            });
        } catch (e) {
            setNotice("Wrong username or password");
        }
    };
    const handleClickRegister = async (e) => {
        e.preventDefault();
        if (
            name == "" ||
            usernameRegister == "" ||
            passwordRegister == "" ||
            repeatPassword == ""
        ) {
            setNoticeRegister("Please fill all information!");
            return;
        }
        if (passwordRegister != repeatPassword) {
            setNoticeRegister("Password and repeat password isn't match!");
            return;
        }
        var data = {
            Name: name,
            Username: usernameRegister,
            Password: passwordRegister,
        };
        try {
            await Axios.post(Root.User.Register, data).then((res) => {
                handleCloseRegisterModal();
                setNotice("Resgister succesful, please log in!");
            });
        } catch (e) {
            setNoticeRegister("Username is used!");
        }
    };
    const handleCloseRegisterModal = () => {
        setOpenRegister(false);
        setName("");
        setNoticeRegister("");
        setPasswordRegister("");
        setRepeatPassword("");
        setUsernameRegister("");
    };

    return (
        <div
            style={{
                backgroundImage: `url(${Background})`,
                backgroundPosition: "center",
                backgrounRepeat: "no-repeat",
                backgroundSize: "cover",
                height: "930px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <div
                style={{
                    width: "500px",
                }}
            >
                <Paper>
                    <Grid
                        container
                        spacing={3}
                        direction={"column"}
                        justify={"center"}
                        alignItems={"center"}
                    >
                        <Grid item>
                            <TextField
                                label="Username"
                                sx={{ width: "400px" }}
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            ></TextField>
                        </Grid>
                        <Grid item>
                            <TextField
                                label="Password"
                                type={"password"}
                                sx={{ width: "400px" }}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            ></TextField>
                        </Grid>
                        <Grid item>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={checked}
                                        onChange={handleChange}
                                        label={"Admin"}
                                        inputProps={{
                                            "aria-label": "primary checkbox",
                                        }}
                                    />
                                }
                                label="Admin"
                            />
                        </Grid>
                        <div>{notice}</div>
                        <Grid item>
                            <Button onClick={handleClickLogin}> Login </Button>
                            <Button
                                onClick={() => {
                                    setOpenRegister(true);
                                }}
                            >
                                {" "}
                                Register{" "}
                            </Button>
                        </Grid>
                    </Grid>
                </Paper>
            </div>
            <Modal
                open={openRegister}
                onClose={() => {
                    setOpenRegister(false);
                }}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <TextField
                        required
                        id="outlined-required"
                        label="Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Usename"
                        value={usernameRegister}
                        onChange={(e) => setUsernameRegister(e.target.value)}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Password"
                        value={passwordRegister}
                        onChange={(e) => setPasswordRegister(e.target.value)}
                        sx={{ width: "400px", marginBottom: "20px" }}
                        type={"password"}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Repeat Password"
                        value={repeatPassword}
                        onChange={(e) => setRepeatPassword(e.target.value)}
                        sx={{ width: "400px", marginBottom: "20px" }}
                        type={"password"}
                    />
                    <div>{noticeRegister}</div>
                    <Button
                        sx={{ marginLeft: "150px" }}
                        onClick={handleClickRegister}
                    >
                        {" "}
                        Register{" "}
                    </Button>
                </Box>
            </Modal>
        </div>
    );
}
