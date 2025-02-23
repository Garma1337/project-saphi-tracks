import {Alert, Box, Typography} from "@mui/material";

const TutorialView = () => {
    return (
        <>
            <Typography variant="h4">Tutorial</Typography>

            <Box my={2}>
                <Alert severity="warning">
                    This section is under construction ...
                </Alert>
            </Box>
        </>
    );
}

export default TutorialView;