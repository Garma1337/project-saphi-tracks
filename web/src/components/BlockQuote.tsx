import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

const Blockquote = ({ text }: { text: string }) => {
    return (
        <Box
            component="blockquote"
            sx={{
                borderLeft: 4,
                borderColor: 'grey.500',
                paddingLeft: 2,
                margin: 2,
                fontStyle: 'italic',
                backgroundColor: 'background.paper',
                color: 'text.secondary'
            }}
        >
            <Typography variant="body1">{text}</Typography>
        </Box>
    );
};

export default Blockquote;