import ApiClient from "../lib/services/apiClient.ts";
import ServiceManager from "../lib/serviceManager.ts";
import Link from "@mui/material/Link";

interface DownloadButtonProps {
    resourceId: number;
    label?: string;
    fallbackFilename?: string;
}

const DownloadResourceLink = (props: DownloadButtonProps) => {
    const apiClient: ApiClient = ServiceManager.createApiClient();

    const extractFilename = (contentDisposition: string): string => {
        let filename = props.fallbackFilename || 'download';

        if (contentDisposition) {
            const match = contentDisposition.match(/filename='?(.+?)'?$/);
            if (match) filename = match[1];
        }

        return filename;
    }

    const initiateDownload = (blob: Blob, fileName: string) => {
        const blobUrl = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = blobUrl;

        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();

        link.remove();
        window.URL.revokeObjectURL(blobUrl);
    }

    const handleDownload = async () => {
        try {
            const response = await apiClient.downloadResource(props.resourceId);

            const filename = extractFilename(response.content_disposition);
            initiateDownload(response.file, filename);
        } catch (error) {
            console.error(`Failed to download resource with id ${props.resourceId}: `, error);
        }
    };

    return (
        <Link onClick={handleDownload}>{props.label || 'Download'}</Link>
    );
};

export default DownloadResourceLink;