from invoice_processor import InvoiceProcessor, InvoiceProcessorConfig

config = InvoiceProcessorConfig(
    api_key= "AIzaSyBc5V_m3cstdCH-zwDKl5q6SLh7UVOCfpY",
    image_dir="path/to/images",
    output_dir="json_outputs"
)

processor = InvoiceProcessor(config)

# For a single image
processor.process_image("invoices/image.png")

# Or for all images in the directory
# processor.process_all_images()
