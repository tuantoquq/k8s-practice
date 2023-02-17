import React from "react";
import { TextField, Grid, Box, Modal, Typography } from "@mui/material";
import CodeEditor from "@uiw/react-textarea-code-editor";

const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 1200,
    height: 500,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
};

export default function DetailMiner(props) {
    const MinerDefault = {
        Name: "",
        RecursiveRange: "",
        InputTables: "",
        GetInputs: "",
        Formula: "",
    };

    return (
        <>
            <Modal
                open={props.status}
                onClose={() => {
                    props.callBack();
                }}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography align="center" variant="h4">
                        Miner Detail
                    </Typography>
                    <Grid container spacing={2}>
                        <Grid item xs={3}>
                            <TextField
                                required
                                id="outlined-required"
                                label="Name"
                                value={
                                    props?.Miner?.Name === undefined
                                        ? MinerDefault.Name
                                        : props.Miner.Name
                                }
                                onChange={(e) => {
                                    props.setValue({
                                        ...props.Miner,
                                        Name: e.target.value,
                                    });
                                }}
                                sx={{
                                    width: "290px",
                                    marginBottom: "20px",
                                }}
                            />
                            <TextField
                                required
                                id="outlined-required"
                                label="Recursive range"
                                value={
                                    props?.Miner?.RecursiveRange === undefined
                                        ? MinerDefault.RecursiveRange
                                        : props.Miner.RecursiveRange
                                }
                                onChange={(e) => {
                                    props.setValue({
                                        ...props.Miner,
                                        RecursiveRange: e.target.value,
                                    });
                                }}
                                sx={{
                                    width: "290px",
                                    marginBottom: "20px",
                                }}
                            />
                            <Typography align="center">Input Tables</Typography>
                            <CodeEditor
                                value={
                                    props?.Miner?.InputTables === undefined
                                        ? MinerDefault.InputTables
                                        : props.Miner.InputTables
                                }
                                language="python"
                                padding={15}
                                style={{
                                    fontSize: 12,
                                    backgroundColor: "#f5f5f5",
                                    fontFamily:
                                        "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
                                    height: "270px",
                                }}
                                onChange={(e) => {
                                    props.setValue({
                                        ...props.Miner,
                                        InputTables: e.target.value,
                                    });
                                }}
                                placeholder={"{'table name': offset}"}
                            />
                        </Grid>
                        <Grid item xs={4.5}>
                            <Typography align="center">
                                Get Input Function
                            </Typography>
                            <CodeEditor
                                value={
                                    props?.Miner?.GetInputs === undefined
                                        ? MinerDefault.GetInputs
                                        : props.Miner.GetInputs
                                }
                                language="python"
                                padding={15}
                                style={{
                                    fontSize: 12,
                                    backgroundColor: "#f5f5f5",
                                    fontFamily:
                                        "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
                                    height: "423px",
                                }}
                                onChange={(e) => {
                                    props.setValue({
                                        ...props.Miner,
                                        GetInputs: e.target.value,
                                    });
                                }}
                            />
                        </Grid>
                        <Grid item xs={4.5}>
                            <Typography align="center">
                                Formula Function
                            </Typography>
                            <CodeEditor
                                value={
                                    props?.Miner?.Formula === undefined
                                        ? MinerDefault.Formula
                                        : props.Miner.Formula
                                }
                                language="python"
                                padding={15}
                                style={{
                                    fontSize: 12,
                                    backgroundColor: "#f5f5f5",
                                    fontFamily:
                                        "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
                                    height: "423px",
                                }}
                                onChange={(e) => {
                                    props.setValue({
                                        ...props.Miner,
                                        Formula: e.target.value,
                                    });
                                }}
                            />
                        </Grid>
                    </Grid>
                </Box>
            </Modal>
        </>
    );
}
