import React from "react";
import { Button, Box, Modal, Typography } from "@mui/material";

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

export default function ConfirmModal(props) {
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
                    <Typography align="center" variant="h6">
                        {props.title}
                    </Typography>
                    <Button
                        variant="contained"
                        color="success"
                        onClick={() => props.onClick()}
                        sx={{ marginLeft: "180px", marginTop: "30px" }}
                    >
                        Yes
                    </Button>
                </Box>
            </Modal>
        </>
    );
}
